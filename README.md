# Jasmin Telnet

Manage Jasmin SMS Gateway's [https://github.com/jookies/jasmin] through telnet


## Install
#### PYPI:
```
pip3 install -U jasmin-telnet
```
#### From Source:
```
git clone https://github.com/BlackOrder/jasmin_telnet.git
cd jasmin_telnet
pip3 install .
```


## Use:

### Import first:

```
from jasmin_telnet.proxy import Proxy as JasminTelnetProxy
```

### Initialize variables:
```

jasmin_proxy = JasminTelnetProxy(
    host=**jasmin_cli_host**,                               # Default: 127.0.0.1
    port=**jasmin_cli_port**,                               # Default: 8990
    timeout=**jasmin_cli_timeout**,                         # Default: 10
    auth=**jasmin_cli_auth**,                               # Default: True
    username=**jasmin_cli_username**,                       # Default: "jcliadmin"
    password=**jasmin_cli_password**,                       # Default: "jclipwd"
    standard_prompt=**jasmin_cli_standard_prompt**,         # Default: "jcli : "
    interactive_prompt=**jasmin_cli_interactive_prompt**,   # Default: "> "
    log_status=True,                                        # Default: False
    logger=self.logger_callback                             # Default: None
)
```

### Sync

##### Single Module
To sync, remove any sub-module not sent and add not existing and update existing.
```
jasmin_proxy.sync(
    module="smppccm",
    sub_modules_data={
        "cid1":{
            "cid":"cid1",
            "username":"someUsername1",
            "host":"127.0.0.1"
        },
        "cid2":{
            "cid":"cid2",
            "username":"someUsername2",
            "host":"127.0.0.2"
        },
        "cid3":{
            "cid":"cid3",
            "username":"someUsername3",
            "host":"127.0.0.3"
        }
    }
)
```

#### Sync All
```
jasmin_proxy.syncAll(
    collection_data={
        "smppccm": {
            "cid1":{
                "cid":"cid1",
                "username":"USERNAME",
                "host":"127.0.0.1"
            },
            "cid2":{
                "cid":"cid2",
                "username":"USERNAME",
                "host":"127.0.0.2"
            },
            "cid3":{
                "cid":"cid3",
                "username":"USERNAME",
                "host":"127.0.0.3"
            }
        },
        "group":{
            "gid1":{
                "gid": "gid1"
            }
        },
        "user":{
            "uid1": {
                "uid": "uid1",
                "gid": "gid1",
                "username": "USERNAME",
                "password": "PASS"
            }
        }
    }
)
```
Beware, any module not included will be flushed.
if you send this:
```
jasmin_proxy.syncAll()
```
or
```
jasmin_proxy.syncAll(collection_data={})
```
or
```
jasmin_proxy.syncAll(collection_data=None)
```
This will flush all of Jasmin configurations.



### Add New
```
jasmin_proxy.add(
    module="user",
    sub_id="uid3",
    options={
                "uid": "uid3",
                "gid": "gid1",
                "username": "USERNAME",
                "password": "PASS"
            }
)
```

### Edit
```
jasmin_proxy.edit(
    module="user",
    sub_id="uid3",
    options={
                "password": "NEW_PASS"
            }
)
```

### Remove
```
jasmin_proxy.remove(
    module="user",
    sub_id="uid3"
)
```

