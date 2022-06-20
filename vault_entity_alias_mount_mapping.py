#!/opt/homebrew/bin/python3

# For each entity in Vault, print entity ID and name.
# For each entity alias, print entity alias name, id and mount.

# to use, set VAULT_ADDR and VAULT_TOKEN environment variablces.

import urllib3
import hvac
from os import environ

urllib3.disable_warnings()

client = hvac.Client(
  url = environ['VAULT_ADDR'],
  token = environ['VAULT_TOKEN'],
  verify=False
)

list_response = client.secrets.identity.list_entities()
entity_ids = list_response['data']['keys']

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
