#!/opt/homebrew/bin/python3

# For each entity in Vault, print entity ID and name.
# For each entity alias, print entity alias name, id and mount.

# to use, set VAULT_ADDR and VAULT_TOKEN environment variablces.

import urllib3
import hvac
import json
import time
from os import environ, _exit, path, times
import sys
import logging

urllib3.disable_warnings()

def get_entity_list(client, active_entities):
  try:
    print("Entities:")
    list_entities_response = client.secrets.identity.list_entities()
    entity_ids = list_entities_response['data']['keys']

    for entity_id in entity_ids:
      read_entity_response = client.secrets.identity.read_entity(
        entity_id=entity_id,
      )
      name = read_entity_response['data']['name']
      print("Entity ID:\t{id}\nEntity Name:\t{name}".format(id=entity_id, name=name))
      if entity_id in active_entities:
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(active_entities[entity_id]))
        print("Active:\t\tyes - first seen " + timestamp)

      #print("Entity ID:\t{id} {active}\nEntity Name:\t{name}".format(active=active, id=entity_id, name=name))

      entity_aliases = read_entity_response['data']['aliases']

      for entity_alias in entity_aliases:
        entity_alias_id = entity_alias['id']
        mount_path = entity_alias['mount_path']
        mount_accessor = entity_alias['mount_accessor']
        mount_type = entity_alias['mount_type']
        entity_alias_name = entity_alias['name']
        print("\t\t\tEntity Alias Name:\t{entity_alias_name}".format(entity_alias_name=entity_alias_name))
        print("\t\t\tEntity Alias ID:\t{entity_alias_id}".format(entity_alias_id=entity_alias_id))
        print("\t\t\tMount Path:\t\t{mount_path}".format(mount_path=mount_path))
        print("\t\t\tMount Accessor:\t\t{mount_accessor}".format(mount_accessor=mount_accessor))
        print("\t\t\tMount Type:\t\t{mount_type}".format(mount_type=mount_type))
        print()

  except:
    pass

  print("------------------------------------------------------------------------")

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
  
  http = http = urllib3.PoolManager()
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

if __name__ == '__main__':

  # logging
  format = "%(asctime)s: %(message)s"
  date_format = "%Y-%m-%d %H:%M:%S %Z"
  logging.basicConfig(format=format, level=logging.INFO, datefmt=date_format)
  logging.info("Starting %s", path.basename(__file__))

  # config
  try:
    vault_addr = environ['VAULT_ADDR']
    logging.info("vault_addr: %s", vault_addr)
  except KeyError:
    logging.error('[error]: `VAULT_ADDR` environment variable not set.')
    sys.exit(1)

  try:
    vault_token = environ['VAULT_TOKEN']
    #logging.debug("vault_token: %s", vault_token)
  except KeyError:
    logging.error('[error]: `VAULT_TOKEN` environment variable not set.')
    sys.exit(1)

  try:
    namespace = environ['VAULT_NAMESPACE']
    logging.info("namespace: %s", namespace)
  except KeyError:
    logging.debug("VAULT_NAMESPACE isn't set.")
    namespace = None

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

  namespaces = [namespace]

  # get all child namespaces in this namespace and list any entities in that namespace
  while namespaces:
    namespace = namespaces.pop(0)

    client = hvac.Client(
      url = vault_addr,
      token = vault_token,
      namespace = namespace,
    )

    print("Namespace: {namespace}".
      format(
        namespace = namespace,
      )
    )

    # get entity list for namespace.
    get_entity_list(client, active_entities)

    namespaces_in_current_namespace = get_namespaces(client)
    
    if namespaces_in_current_namespace is not None:
      for key, value in namespaces_in_current_namespace.items():
        child_namespace = value['path']
        namespaces.append(child_namespace)
        #print(child_namespace)
