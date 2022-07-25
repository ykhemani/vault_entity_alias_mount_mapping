![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/ykhemani/vault_entity_alias_mount_mapping?style=plastic)

# vault_entity_alias_mount_mapping

[vault_entity_alias_mount_mapping.py](vault_entity_alias_mount_mapping.py) uses the [Python](https://www.python.org/) [hvac](https://hvac.readthedocs.io/en/stable/index.html) library to get a list of entities in your [HashiCorp](https://hashicorp.com) [Vault](https://vaultproject.io) cluster. 

For each entity, `vault_entity_alias_mount_mapping` outputs the entity ID and name. For each alias of that entity, the script outputs the alias name, alias ID and mount path.

For clusters running Vault 1.11.0, `vault_entity_alias_mount_mapping` also indicates whether the entity has been active in the last year, and also when the entity was first active in that time period. Note that this relies on [Activity Export API](https://www.vaultproject.io/api-docs/system/internal-counters#activity-export), which was introduced in Vault 1.11.0 and is presently in Tech Preview.

## Use:

### Run with python

#### Prerequisites

To run with Python 3, install the Python [hvac](https://hvac.readthedocs.io/en/stable/index.html) module if it isn't already installed.

```
pip3 install -r requirements.txt
```

`vault_entity_alias_mount_mapping` has been tested with:
* [Python](https://www.python.org/) 3.9.10
* [hvac](https://hvac.readthedocs.io/en/stable/overview.html) 0.11.2
* [HashiCorp](https://hashicorp.com/) [Vault](https://vaultproject.io) 1.11.0

#### Usage:

`vault_entity_alias_mount_mapping` may be run by specifying environment variables or by passing command line arguments. 

```
$ ./vault_entity_alias_mount_mapping.py -h
usage: vault_entity_alias_mount_mapping.py 
  [-h] [--vault_addr VAULT_ADDR]
  [--vault_token VAULT_TOKEN]
  [--vault_namespace VAULT_NAMESPACE]
  [--format {json,text,csv}]
  [--log_level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
  [--version]

vault_entity_alias_mount_mapping.py provides a list of entities in your HashiCorp Vault cluster.

optional arguments:
  -h, --help
    show this help message and exit
  --vault_addr VAULT_ADDR, -vault_address VAULT_ADDR, --address VAULT_ADDR, -address VAULT_ADDR
    Vault Address.
  --vault_token VAULT_TOKEN, -vault_token VAULT_TOKEN, --token VAULT_TOKEN, -token VAULT_TOKEN
    Vault Token.
  --vault_namespace VAULT_NAMESPACE, -vault_namespace VAULT_NAMESPACE, --namespace VAULT_NAMESPACE, -namespace VAULT_NAMESPACE
    Optional: Vault Namespace.
  --format {json,text,csv}, -format {json,text,csv}
    Optional: Output format. Default: text.
  --log_level {CRITICAL,ERROR,WARNING,INFO,DEBUG}, -log_level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
    Optional: Log level. Default: INFO.
  --version, -version, -v
    Show version and exit.
```

You must specify the Vault Address and Vault Token.

You will need a policy that enables you to list and read identity data attached to your Vault token for the specified namespace and all child namespaces.

Optionally, specify the Vault Namespace to authenticate against the specified namespace.

#### Example run:

```
VAULT_ADDR=${VAULT_ADDR} \
  VAULT_TOKEN=${VAULT_TOKEN} \
  python3 ./vault_entity_alias_mount_mapping.py
```

#### Example Output:
```
$ VAULT_ADDR=${VAULT_ADDR} \
>   VAULT_TOKEN=${VAULT_TOKEN} \
>   python3 ./vault_entity_alias_mount_mapping.py
2022-07-24 01:02:58 UTC: Starting vault_entity_alias_mount_mapping.py
2022-07-24 01:02:58 UTC: vault_addr: https://vault.example.com:8200
--------------------------------------------------------------------------------
Vault Entity Alias Mapping
--------------------------------------------------------------------------------

Namespace: None

Entities:
Entity ID:	541345d0-1d00-1f06-2704-083685bf24a4
Entity Name:	wildly-easy-burro
Active:		yes - first seen 2022-07-20 18:00:32 UTC
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

--------------------------------------------------------------------------------

Namespace: ns1/

Entities:
Entity ID:	32c7c515-728c-05a7-85d5-39812613416f
Entity Name:	early-funny-foal
			Entity Alias Name:	early-funny-foal
			Entity Alias ID:	d843f0ff-5f2e-0a3d-28b0-93ae1c082c42
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_deb23053
			Mount Type:		userpass

--------------------------------------------------------------------------------

Namespace: ns2/

Entities:
Entity ID:	2d8948b6-e9ba-ac1f-d84a-017f708e861c
Entity Name:	sadly-fine-gull
			Entity Alias Name:	sadly-fine-gull
			Entity Alias ID:	bdf822e1-6712-f294-fad9-1a8d4ad19cb1
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_0ca79868
			Mount Type:		userpass

Entity ID:	3bd62b2e-29ad-268f-74f6-19fbe920354c
Entity Name:	entity_b9d105db
Active:		yes - first seen 2022-06-26 01:28:29 UTC
			Entity Alias Name:	daily-handy-shrimp
			Entity Alias ID:	d288f725-16d4-ffce-6efd-6f8f081149b7
			Mount Path:		auth/userpass/
			Mount Accessor:		auth_userpass_0ca79868
			Mount Type:		userpass


--------------------------------------------------------------------------------

Namespace: ns1/ns1-a/

Entities:
Namespace: ns1/ns1-b/

Entities:
Namespace: ns1/ns1-b/ns1-b-i/

Entities:
Namespace: ns1/ns1-b/ns1-b-ii/

Entities:

```

#### Example with JSON output:
```
./vault_entity_alias_mount_mapping.py \
  -namespace=ns1 \
  -format=json \
  -log_level WARNING
```

```
$ ./vault_entity_alias_mount_mapping.py \
>   -namespace=ns1 \
>   -format=json \
>   -log_level WARNING
[
  {
    "namespace_id": "",
    "namespace_name": "ns1",
    "entities": [
      {
        "entity_id": "32c7c515-728c-05a7-85d5-39812613416f",
        "entity_name": "early-funny-foal",
        "active": false,
        "first_seen": null,
        "entity_aliases": [
          {
            "entity_alias_id": "d843f0ff-5f2e-0a3d-28b0-93ae1c082c42",
            "entity_alias_name": "early-funny-foal",
            "mount_path": "auth/userpass/",
            "mount_accessor": "auth_userpass_deb23053",
            "mount_type": "userpass"
          }
        ]
      },
      {
        "entity_id": "66921d6f-c6fb-e715-6c75-cdcc8860d4ab",
        "entity_name": "nearly-wise-magpie",
        "active": false,
        "first_seen": null,
        "entity_aliases": [
          {
            "entity_alias_id": "165b5ca7-6f19-ddbe-f472-a8bb1635f15d",
            "entity_alias_name": "nearly-wise-magpie",
            "mount_path": "auth/userpass/",
            "mount_accessor": "auth_userpass_deb23053",
            "mount_type": "userpass"
          }
        ]
      },
      {
        "entity_id": "84283942-dc9a-6841-d659-ac3906daaa16",
        "entity_name": "overly-up-racer",
        "active": false,
        "first_seen": null,
        "entity_aliases": [
          {
            "entity_alias_id": "37547543-8a06-b30d-460e-033006728488",
            "entity_alias_name": "overly-up-racer",
            "mount_path": "auth/userpass/",
            "mount_accessor": "auth_userpass_deb23053",
            "mount_type": "userpass"
          }
        ]
      }
    ]
  },
  {
    "namespace_id": "XR3hl",
    "namespace_name": "ns1/ns1-a/",
    "entities": null
  },
  {
    "namespace_id": "S9MYX",
    "namespace_name": "ns1/ns1-b/",
    "entities": null
  },
  {
    "namespace_id": "C9zbp",
    "namespace_name": "ns1/ns1-c/",
    "entities": null
  },
  {
    "namespace_id": "9ndZC",
    "namespace_name": "ns1/ns1-b/ns1-b-i/",
    "entities": null
  },
  {
    "namespace_id": "hhpyR",
    "namespace_name": "ns1/ns1-b/ns1-b-ii/",
    "entities": null
  }
]
```

#### Example CSV Output:
```
$ ./vault_entity_alias_mount_mapping.py -format=csv -log_level WARNING
namespace_id,namespace_name,entity_id,entity_name,active,first_seen,entity_alias_id,entity_alias_name,mount_path,mount_accessor,mount_type
,,541345d0-1d00-1f06-2704-083685bf24a4,wildly-easy-burro,True,2022-07-20 18:00:32 UTC,2ceece6c-1507-dfe1-73eb-2730387df873,wildly-easy-burro,auth/userpass/,auth_userpass_5b042f94,userpass
,,c66f7bd3-55cb-6199-9c47-fb1df0244943,deeply-key-hippo,False,,7d49b101-9bb7-1461-5dfd-748f492aab49,deeply-key-hippo,auth/userpass/,auth_userpass_5b042f94,userpass
,,caa311b9-ac0f-45ea-f72e-342e02560415,firmly-secure-lemur,False,,256f4ae3-0b84-924d-e25d-2823abaa74c0,firmly-secure-lemur,auth/userpass/,auth_userpass_5b042f94,userpass
be5QT,ns1/,32c7c515-728c-05a7-85d5-39812613416f,early-funny-foal,False,,d843f0ff-5f2e-0a3d-28b0-93ae1c082c42,early-funny-foal,auth/userpass/,auth_userpass_deb23053,userpass
be5QT,ns1/,66921d6f-c6fb-e715-6c75-cdcc8860d4ab,nearly-wise-magpie,False,,165b5ca7-6f19-ddbe-f472-a8bb1635f15d,nearly-wise-magpie,auth/userpass/,auth_userpass_deb23053,userpass
be5QT,ns1/,84283942-dc9a-6841-d659-ac3906daaa16,overly-up-racer,False,,37547543-8a06-b30d-460e-033006728488,overly-up-racer,auth/userpass/,auth_userpass_deb23053,userpass
bX58H,ns2/,2d8948b6-e9ba-ac1f-d84a-017f708e861c,sadly-fine-gull,False,,bdf822e1-6712-f294-fad9-1a8d4ad19cb1,sadly-fine-gull,auth/userpass/,auth_userpass_0ca79868,userpass
bX58H,ns2/,3b5aceab-cde0-bd68-12f0-976ff380baeb,lively-crack-shark,False,,f06567bf-6353-8066-0281-a2f80b2568aa,lively-crack-shark,auth/userpass/,auth_userpass_0ca79868,userpass
bX58H,ns2/,3bd62b2e-29ad-268f-74f6-19fbe920354c,entity_b9d105db,True,2022-06-26 01:28:29 UTC,d288f725-16d4-ffce-6efd-6f8f081149b7,daily-handy-shrimp,auth/userpass/,auth_userpass_0ca79868,userpass
gzwYv,ns3/,6a02b17e-63c0-3f09-2c21-abd693107c84,safely-key-filly,False,,b96a92d3-e807-c40b-741d-516acbffc69d,safely-key-filly,auth/userpass/,auth_userpass_5557a4f5,userpass
gzwYv,ns3/,996af036-01cb-47e8-68ce-1bb15a494b08,daily-strong-piglet,False,,5b9b49f7-9a34-492c-caca-41d76a30ed52,daily-strong-piglet,auth/userpass/,auth_userpass_5557a4f5,userpass
gzwYv,ns3/,c6944630-af31-9ced-d485-44cd2a50a3be,wholly-causal-trout,False,,e10e04fb-ac73-7cc0-8bde-92a219c73682,wholly-causal-trout,auth/userpass/,auth_userpass_5557a4f5,userpass
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
  ykhemani/vault_entity_alias_mount_mapping:0.0.4
```

## Building Docker Image

For example:

```
docker build -t ykhemani/vault_entity_alias_mount_mapping:0.0.4 .
```

---
