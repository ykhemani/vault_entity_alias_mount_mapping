![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/ykhemani/vault_entity_alias_mount_mapping?style=plastic)

# vault_entity_alias_mount_mapping

[vault_entity_alias_mount_mapping.py](vault_entity_alias_mount_mapping.py) uses the [Python](https://www.python.org/) [hvac](https://hvac.readthedocs.io/en/stable/index.html) library to get a list of entities in your [HashiCorp](https://hashicorp.com) [Vault](https://vaultproject.io) cluster. 

For each entity, `vault_entity_alias_mount_mapping` outputs the entity ID and name. For each alias of that entity, the script outputs the alias name, alias ID and mount path.

For clusters running Vault 1.11.0, `vault_entity_alias_mount_mapping` also indicates whether the entity has been active in the last year, and also when the entity was first active in that time period. Note that this relies on [Activity Export API](https://www.vaultproject.io/api-docs/system/internal-counters#activity-export), which was introduced in Vault 1.11.0 and is in Tech Preview.

## Use:

### Run with python

Install the Python [hvac](https://hvac.readthedocs.io/en/stable/index.html) if it isn't already installed.

```
pip3 install -r requirements.txt
```

Set your `VAULT_ADDR` and `VAULT_TOKEN` environment variables to allow vault_entity_alias_mount_mapping to authenticate with your Vault cluster. You will need a policy that enables you to list and read identity data attached to your Vault token for the specified namespace and all child namespaces.

Optionally set your `VAULT_NAMESPACE` environment variable to authenticate against the specified namespace.

```
VAULT_ADDR=${VAULT_ADDR} \
  VAULT_TOKEN=${VAULT_TOKEN} \
  VAULT_NAMESPACE=${VAULT_NAMESPACE} \
  python3 ./vault_entity_alias_mount_mapping.py
```

#### Example Output:
```
$ VAULT_ADDR=${VAULT_ADDR} \
>   VAULT_TOKEN=${VAULT_TOKEN} \
>   python3 ./vault_entity_alias_mount_mapping.py
2022-07-20 21:25:57 UTC: Starting vault_entity_alias_mount_mapping.py
2022-07-20 21:25:57 UTC: vault_addr: https://vault.example.com:8200
Namespace: None
Entities:
Entity ID:	541345d0-1d00-1f06-2704-083685bf24a4
Entity Name:	wildly-easy-burro
Active:		yes - first seen Wed, 20 Jul 2022 18:00:32
			Entity Alias Name:	wildly-easy-burro
			Entity Alias ID:	2ceece6c-1507-dfe1-73eb-2730387df873
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_5b042f94
			Mount Type:		userpass

Entity ID:	c66f7bd3-55cb-6199-9c47-fb1df0244943
Entity Name:	deeply-key-hippo
			Entity Alias Name:	deeply-key-hippo
			Entity Alias ID:	7d49b101-9bb7-1461-5dfd-748f492aab49
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_5b042f94
			Mount Type:		userpass

Entity ID:	caa311b9-ac0f-45ea-f72e-342e02560415
Entity Name:	firmly-secure-lemur
			Entity Alias Name:	firmly-secure-lemur
			Entity Alias ID:	256f4ae3-0b84-924d-e25d-2823abaa74c0
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_5b042f94
			Mount Type:		userpass

------------------------------------------------------------------------
Namespace: ns1/
Entities:
Entity ID:	32c7c515-728c-05a7-85d5-39812613416f
Entity Name:	early-funny-foal
			Entity Alias Name:	early-funny-foal
			Entity Alias ID:	d843f0ff-5f2e-0a3d-28b0-93ae1c082c42
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_deb23053
			Mount Type:		userpass

Entity ID:	66921d6f-c6fb-e715-6c75-cdcc8860d4ab
Entity Name:	nearly-wise-magpie
			Entity Alias Name:	nearly-wise-magpie
			Entity Alias ID:	165b5ca7-6f19-ddbe-f472-a8bb1635f15d
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_deb23053
			Mount Type:		userpass

Entity ID:	84283942-dc9a-6841-d659-ac3906daaa16
Entity Name:	overly-up-racer
			Entity Alias Name:	overly-up-racer
			Entity Alias ID:	37547543-8a06-b30d-460e-033006728488
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_deb23053
			Mount Type:		userpass

------------------------------------------------------------------------
Namespace: ns2/
Entities:
Entity ID:	2d8948b6-e9ba-ac1f-d84a-017f708e861c
Entity Name:	sadly-fine-gull
			Entity Alias Name:	sadly-fine-gull
			Entity Alias ID:	bdf822e1-6712-f294-fad9-1a8d4ad19cb1
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_0ca79868
			Mount Type:		userpass

Entity ID:	3b5aceab-cde0-bd68-12f0-976ff380baeb
Entity Name:	lively-crack-shark
			Entity Alias Name:	lively-crack-shark
			Entity Alias ID:	f06567bf-6353-8066-0281-a2f80b2568aa
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_0ca79868
			Mount Type:		userpass

Entity ID:	3bd62b2e-29ad-268f-74f6-19fbe920354c
Entity Name:	entity_b9d105db
Active:		yes - first seen Sun, 26 Jun 2022 01:28:29
			Entity Alias Name:	daily-handy-shrimp
			Entity Alias ID:	d288f725-16d4-ffce-6efd-6f8f081149b7
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_0ca79868
			Mount Type:		userpass

------------------------------------------------------------------------
Namespace: ns3/
Entities:
Entity ID:	6a02b17e-63c0-3f09-2c21-abd693107c84
Entity Name:	safely-key-filly
			Entity Alias Name:	safely-key-filly
			Entity Alias ID:	b96a92d3-e807-c40b-741d-516acbffc69d
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_5557a4f5
			Mount Type:		userpass

Entity ID:	996af036-01cb-47e8-68ce-1bb15a494b08
Entity Name:	daily-strong-piglet
			Entity Alias Name:	daily-strong-piglet
			Entity Alias ID:	5b9b49f7-9a34-492c-caca-41d76a30ed52
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_5557a4f5
			Mount Type:		userpass

Entity ID:	c6944630-af31-9ced-d485-44cd2a50a3be
Entity Name:	wholly-causal-trout
			Entity Alias Name:	wholly-causal-trout
			Entity Alias ID:	e10e04fb-ac73-7cc0-8bde-92a219c73682
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_5557a4f5
			Mount Type:		userpass

------------------------------------------------------------------------
Namespace: ns1/ns1-a/
Entities:
------------------------------------------------------------------------
Namespace: ns1/ns1-b/
Entities:
------------------------------------------------------------------------
Namespace: ns1/ns1-c/
Entities:
------------------------------------------------------------------------
Namespace: ns1/ns1-b/ns1-b-i/
Entities:
------------------------------------------------------------------------
Namespace: ns1/ns1-b/ns1-b-ii/
Entities:
------------------------------------------------------------------------
```

#### With a namespace
```
$ VAULT_ADDR=${VAULT_ADDR} \
>   VAULT_TOKEN=${VAULT_TOKEN} \
>   VAULT_NAMESPACE=${VAULT_NAMESPACE} \
>   python3 ./vault_entity_alias_mount_mapping.py

2022-07-20 21:26:39 UTC: Starting vault_entity_alias_mount_mapping.py
2022-07-20 21:26:39 UTC: vault_addr: https://vault.example.com:8200
2022-07-20 21:26:39 UTC: namespace: ns2
Namespace: ns2
Entities:
Entity ID:	2d8948b6-e9ba-ac1f-d84a-017f708e861c
Entity Name:	sadly-fine-gull
			Entity Alias Name:	sadly-fine-gull
			Entity Alias ID:	bdf822e1-6712-f294-fad9-1a8d4ad19cb1
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_0ca79868
			Mount Type:		userpass

Entity ID:	3b5aceab-cde0-bd68-12f0-976ff380baeb
Entity Name:	lively-crack-shark
			Entity Alias Name:	lively-crack-shark
			Entity Alias ID:	f06567bf-6353-8066-0281-a2f80b2568aa
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_0ca79868
			Mount Type:		userpass

Entity ID:	3bd62b2e-29ad-268f-74f6-19fbe920354c
Entity Name:	entity_b9d105db
Active:		yes - first seen Sun, 26 Jun 2022 01:28:29
			Entity Alias Name:	daily-handy-shrimp
			Entity Alias ID:	d288f725-16d4-ffce-6efd-6f8f081149b7
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_0ca79868
			Mount Type:		userpass

------------------------------------------------------------------------
```

### Run with Docker

![Docker Image Version (latest by date)](https://img.shields.io/docker/v/ykhemani/vault_entity_alias_mount_mapping?style=plastic)

You can also run [vault_entity_alias_mount_mapping](https://hub.docker.com/r/ykhemani/vault_entity_alias_mount_mapping) with Docker. For example:
```
docker run \
  -e VAULT_ADDR=${VAULT_ADDR} \
  -e VAULT_TOKEN=${VAULT_TOKEN} \
  -e VAULT_NAMESPACE=${VAULT_NAMESPACE} \
  --rm \
  --name 'vault_entity_alias_mount_mapping' \
  ykhemani/vault_entity_alias_mount_mapping:0.0.3
```

## Building Docker Image

For example:

```
docker build -t ykhemani/vault_entity_alias_mount_mapping:0.0.3 .
```

---
