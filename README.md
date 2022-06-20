# vault_entity_alias_mount_mapping

[vault_entity_alias_mount_mapping.py](vault_entity_alias_mount_mapping.py) uses the Python [hvac](https://hvac.readthedocs.io/en/stable/index.html) library to get a list of entities from [HashiCorp](https://hashicorp.com) [Vault](https://vaultproject.io). For each entity, the script lists the entity ID and name. For each alias to that entity, the script list the alias name, alias ID and mount path.

## Use:
Install the Python [hvac](https://hvac.readthedocs.io/en/stable/index.html) if it isn't already installed.

Authenticate with Vault and set your `VAULT_ADDR` and `VAULT_TOKEN` environment variables. You will need a policy that enables you to list and read identity data attached to your Vault token.

## Example Output:
```
$ python3 vault_entity_alias_mount_mapping.py 
Entity ID:	564f8234-f23a-4e21-3ebf-34ca63c77e6c
Entity Name:	entity_e1abcdc2
			Entity Alias Name:	test
			Entity Alias ID:	391bd575-e1c7-e8d6-4e89-4321242d68fc
			Mount Path:		auth/userpass/


Entity ID:	6a29ac2d-0a98-b36c-9284-280cee3ace58
Entity Name:	obi-wan
			Entity Alias Name:	obiwan
			Entity Alias ID:	007c99bc-ebe2-3878-7276-496d534edb46
			Mount Path:		auth/userpass/

			Entity Alias Name:	obiwan@example.com
			Entity Alias ID:	1f2d38d5-c53c-3175-2e78-de70cd2dc02b
			Mount Path:		auth/okta/
```

---
