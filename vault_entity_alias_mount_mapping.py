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
    list_entities_response = client.secrets.identity.list_entities()
    entity_ids = list_entities_response['data']['keys']

    for entity_id in entity_ids:
      read_response = client.secrets.identity.read_entity(
            entity_id=entity_id,
      )
      name = read_response['data']['name']
      print("Entity ID:\t{id}\nEntity Name:\t{name}".format(id=entity_id, name=name))

      entity_aliases = read_response['data']['aliases']

      for entity_alias in entity_aliases:
        entity_alias_id = entity_alias['id']
        mount_path = entity_alias['mount_path']
        entity_alias_name = entity_alias['name']
        print("\t\t\tEntity Alias Name:\t{entity_alias_name}\n\t\t\tEntity Alias ID:\t{entity_alias_id}\n\t\t\tMount Path:\t\t{mount_path}\n".
          format(entity_alias_name=entity_alias_name,
                entity_alias_id=entity_alias_id, 
                mount_path=mount_path))
      print('')

  except:
    logging.error("[ERROR]: Unable to get entities.")

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

  # Vault Client
  client = hvac.Client(
    url = vault_addr,
    token = vault_token
  )

  print("Namespace: root\nEntities:")
  get_entity_list(client)
  print("------------------------------------------------------------------------")

  # get namespaces
  try:
    list_namespaces_response = client.sys.list_namespaces()
    namespaces = list_namespaces_response['data']['key_info']

    for namespace in namespaces:
      print("Namespace: {namespace}".format(namespace=namespace))
      print("Entities: ")
      ns_client = hvac.Client(
        url = vault_addr,
        token = vault_token,
        namespace = namespace
      )
      get_entity_list(ns_client)
      print("------------------------------------------------------------------------")
  except:
    logging.error("[ERROR]: Unable to list namespaces.")

