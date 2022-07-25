#!/usr/bin/env python3

# For each entity in Vault, print entity ID and name.
# For each entity alias, print entity alias name, id and mount.

# to use, set VAULT_ADDR and VAULT_TOKEN environment variablces.

import urllib3
import hvac
import json
import csv
import time
from os import environ, _exit, path, times
import sys
import logging
import argparse
from EnvDefault import env_default

version = '0.0.4'

urllib3.disable_warnings()

def append_output_text(next):
  global output_text
  output_text += next

def append_output_list(next):
  global output_list
  output_list.append(next)

def get_entity_list(client, active_entities, namespace_id, namespace_name):
  global output_line
  global output_csv
  try:
    append_output_text("Entities:\n")
    list_entities_response = client.secrets.identity.list_entities()
    entity_ids = list_entities_response['data']['keys']
    # entities list to return for json output
    entities = []

    for entity_id in entity_ids:
      read_entity_response = client.secrets.identity.read_entity(
        entity_id=entity_id,
      )
      name = read_entity_response['data']['name']
      append_output_text("Entity ID:\t{id}\nEntity Name:\t{name}\n".format(id=entity_id, name=name))

      if entity_id in active_entities:
        active = True
        timestamp = time.strftime(date_format, time.gmtime(active_entities[entity_id]))
        append_output_text("Active:\t\tyes - first seen " + timestamp + "\n")
      else:
        active = False
        timestamp = None

      #print("Entity ID:\t{id} {active}\nEntity Name:\t{name}".format(active=active, id=entity_id, name=name))

      entity_aliases = read_entity_response['data']['aliases']

      entity_aliases_list = []
      for entity_alias in entity_aliases:
        entity_alias_id = entity_alias['id']
        mount_path = entity_alias['mount_path']
        mount_accessor = entity_alias['mount_accessor']
        mount_type = entity_alias['mount_type']
        entity_alias_name = entity_alias['name']
        append_output_text("\t\t\tEntity Alias Name:\t{entity_alias_name}\n".format(entity_alias_name=entity_alias_name))
        append_output_text("\t\t\tEntity Alias ID:\t{entity_alias_id}\n".format(entity_alias_id=entity_alias_id))
        append_output_text("\t\t\tMount Path:\t\t{mount_path}\n".format(mount_path=mount_path))
        append_output_text("\t\t\tMount Accessor:\t\t{mount_accessor}\n".format(mount_accessor=mount_accessor))
        append_output_text("\t\t\tMount Type:\t\t{mount_type}\n".format(mount_type=mount_type))
        append_output_text("\n")
        entity_aliases_list.append(
          {
            'entity_alias_id' : entity_alias_id,
            'entity_alias_name' : entity_alias_name,
            'mount_path' : mount_path,
            'mount_accessor' : mount_accessor,
            'mount_type' : mount_type
          }
        )

        # csv format:
        # namespace_id, namespace_name, entity_id, entity_name, active, first_seen, entity_alias_id, entity_alias_name, mount_path, mount_accessor, mount_type
        output_csv.append(
          [
            namespace_id,
            namespace_name,
            entity_id,
            name,
            active,
            timestamp,
            entity_alias_id,
            entity_alias_name,
            mount_path,
            mount_accessor,
            mount_type
          ]
        )

      entities.append(
        {
          'entity_id' : entity_id,
          'entity_name' : name,
          'active' : active,
          'first_seen' : timestamp,
          'entity_aliases' : entity_aliases_list
        }
      )

    append_output_text("\n" + output_line + "\n")
    return(entities)
  except Exception as e:
    pass

def get_namespaces(client):
  # get namespaces
  try:
    list_namespaces_response = client.sys.list_namespaces()
    namespaces = list_namespaces_response['data']['key_info']
    return namespaces
  except:
    logging.debug("Unable to list namespaces.")

def health_check(client):
  # get Vault health
  error = 0
  try:
    health = client.sys.read_health_status(method='GET')
    if not health['initialized']:
      logging.error('[error]: Vault is not initialized.')
      error = 1
    if health['sealed']:
      logging.error('[error]: Vault is sealed.')
      error = 1
    if error == 1:
      sys.exit(1)
    return(health['version'])
  except Exception as e:
    logging.error(e)
    logging.error('[error]: Unable to read Vault health.')
    sys.exit(1)

def get_active_entities(vault_addr, vault_token):
  # experimental
  # see https://www.vaultproject.io/api-docs/system/internal-counters#activity-export

  #active_entities_list = []
  active_entities_dict = {}

  now = int(time.time())
  start_time = now - (365 * 24 * 60 * 60) # one year ago

  activity_url = vault_addr + '/v1/sys/internal/counters/activity/export?end_time=' + str(now) + '&start_time=' + str(start_time)
  logging.debug("activity url: %s", activity_url)
  
  http = urllib3.PoolManager()
  response = http.request(
    'GET', 
    activity_url,
    headers = {
      'X-Vault-Token' : vault_token
    }
  )
  data = response.data.decode("utf-8")
  for entity in data.splitlines():
    logging.debug(entity)
    entity_json = json.loads(entity)
    entity_id = entity_json['client_id']
    timestamp = entity_json['timestamp']
    #active_entities_list.append(json.loads(entity)['client_id'])
    active_entities_dict[entity_id] = timestamp
  #return(active_entities_list)
  return(active_entities_dict)

help_indent_formatter = lambda prog: argparse.RawTextHelpFormatter(
  prog,
  max_help_position=4, 
  indent_increment=2,
  width=80
)

if __name__ == '__main__':

  parser = argparse.ArgumentParser(
    formatter_class=help_indent_formatter,
    description = 'vault_entity_alias_mount_mapping.py provides a list of entities in your HashiCorp Vault cluster.',
  )

  parser.add_argument(
    '--vault_addr', '-vault_address', '--address', '-address',
    action = env_default('VAULT_ADDR'),
    help = 'Vault Address.',
    required = True,
  )

  parser.add_argument(
    '--vault_token', '-vault_token', '--token', '-token',
    action = env_default('VAULT_TOKEN'),
    help = 'Vault Token.',
    required = True
  )

  parser.add_argument(
    '--vault_namespace', '-vault_namespace', '--namespace', '-namespace',
    action = env_default('VAULT_NAMESPACE'),
    help = 'Optional: Vault Namespace.',
    required = False,
    default = None
  )

  parser.add_argument(
    '--format', '-format',
    action = env_default('FORMAT'),
    help = 'Optional: Output format. Default: text.',
    choices = ['json', 'text', 'csv'],
    required = False,
    default = None
  )

  parser.add_argument(
    '--log_level', '-log_level',
    action = env_default('LOG_LEVEL'),
    help = 'Optional: Log level. Default: INFO.',
    choices = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
    required = False
  )

  parser.add_argument(
    '--version', '-version', '-v',
    help='Show version and exit.',
    action='version',
    version=f"{version}"
  )

  args = parser.parse_args()

  # logging
  format = "%(asctime)s: %(message)s"
  date_format = "%Y-%m-%d %H:%M:%S %Z"
  logging.basicConfig(format=format, level=logging.INFO, datefmt=date_format)

  if args.log_level == 'CRITICAL':
    logging.getLogger().setLevel(logging.CRITICAL)
  elif args.log_level == 'ERROR':
    logging.getLogger().setLevel(logging.ERROR)
  elif args.log_level == 'WARNING':
    logging.getLogger().setLevel(logging.WARNING)
  elif args.log_level == 'INFO':
    logging.getLogger().setLevel(logging.INFO)
  elif args.log_level == 'DEBUG':
    logging.getLogger().setLevel(logging.DEBUG)

  logging.debug("Log level set to %s", args.log_level)
  logging.info("Starting %s", path.basename(__file__))

  # config
  try:
    vault_addr = args.vault_addr
    logging.info("vault_addr: %s", vault_addr)
  except Exception as e:
    logging.error(e)
    logging.error('[error]: Vault Address not specified.')
    sys.exit(1)

  try:
    vault_token = args.vault_token
  except Exception as e:
    logging.error(e)
    logging.error('[error]: Vault token not specified.')
    sys.exit(1)

  namespace = args.vault_namespace
  if namespace is not None:
    logging.info("namespace: %s", namespace)
  else:
    logging.debug("Vault namespace not specified.")

  # Vault Client
  try:
    client = hvac.Client(
      url = vault_addr,
      token = vault_token,
      namespace = namespace,
    )
  except:
    logging.error("Unable to connect to Vault cluster %s", vault_addr)
    sys.exit(1)

  vault_version = health_check(
    hvac.Client(url = vault_addr)
  )
  if vault_version.startswith('1.11'):
    active_entities = get_active_entities(vault_addr, vault_token) # we don't pass namespace because the Activity Export API appears to only work on the root namespace.
  else:
    active_entities = {}

  #namespaces = [namespace]
  # namespaces is a dict of namespace_id : namespace_name
  namespaces = {'' : namespace} # we don't know the namespace id of the provided namespace, so we set it to empty.

  # outputs
  output_line = "--------------------------------------------------------------------------------\n"
  output_text = ''
  append_output_text(output_line + "Vault Entity Alias Mapping\n" + output_line + "\n")
  output_list = []

  # csv format:
  # namespace_id, namespace_name, entity_id, entity_name, active, first_seen, entity_alias_id, entity_alias_name, mount_path, mount_accessor, mount_type
  output_csv  = [
    [
      'namespace_id',
      'namespace_name',
      'entity_id',
      'entity_name',
      'active',
      'first_seen',
      'entity_alias_id',
      'entity_alias_name',
      'mount_path', 
      'mount_accessor', 
      'mount_type'
    ]
  ]

  # get all child namespaces in this namespace and list any entities in that namespace
  while bool(namespaces):
    #namespace = namespaces.pop(0)
    #namespace_id = list(namespaces.keys()[0])
    namespace_id = next(iter(namespaces))
    namespace_name = namespaces[namespace_id]
    del namespaces[namespace_id]
    #print(namespaces)

    client = hvac.Client(
      url = vault_addr,
      token = vault_token,
      namespace = namespace_name,
    )

    append_output_text("Namespace: {namespace}\n\n".
      format(
        namespace = namespace_name,
      )
    )
    
    # get entity list for namespace.
    entities = get_entity_list(client, active_entities, namespace_id, namespace_name)
    append_output_list(
      {
        'namespace_id' : namespace_id,
        'namespace_name' : namespace_name,
        'entities' : entities
      }
    )

    namespaces_in_current_namespace = get_namespaces(client)
    
    if namespaces_in_current_namespace is not None:
      for key, value in namespaces_in_current_namespace.items():
        child_namespace_id = value['id']
        child_namespace_name = value['path']
        #namespaces.append(child_namespace)
        namespaces[child_namespace_id] = child_namespace_name
        #print(child_namespace)
        #print("added " + child_namespace_id + " " + child_namespace_name)

  if args.format == 'json':
    print(json.dumps(output_list, indent = 2))
  elif args.format == 'csv':
    csv_writer = csv.writer(sys.stdout)
    csv_writer.writerows(output_csv)
  else: # elif args.format == 'text':
    print(output_text)

  sys.exit(0)
