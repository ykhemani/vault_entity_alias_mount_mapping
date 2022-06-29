#!/opt/homebrew/bin/python3

# For each entity in Vault, print entity ID and name.
# For each entity alias, print entity alias name, id and mount.

# to use, set VAULT_ADDR and VAULT_TOKEN environment variablces.

import urllib3
import hvac
from os import environ, _exit, path
import sys
import logging

urllib3.disable_warnings()

def get_entity_list(client):
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
      print('')

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
    get_entity_list(client)

    namespaces_in_current_namespace = get_namespaces(client)
    
    if namespaces_in_current_namespace is not None:
      for key, value in namespaces_in_current_namespace.items():
        child_namespace = value['path']
        namespaces.append(child_namespace)
        #print(child_namespace)
