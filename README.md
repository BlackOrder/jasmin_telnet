# Jasmin Telnet

Manage [Jasmin SMS Gateway](https://github.com/jookies/jasmin)'s configurations through telnet

I wrote some of it and collected most of from: [jasmin-api](https://github.com/jookies/jasmin-api) and [jasmin-web-panel](https://github.com/101t/jasmin-web-panel).

Also some of the logic is ported from this PHP package [jasmin-web](https://github.com/nnikitos95/jasmin-web) by [nnikitos95](https://github.com/nnikitos95)

## Table of Contents

1. **[Installation Instructions](#installation-instructions)**
    + **[PYPI](#pypi)**
    + **[From Source](#from-source)**
2. **[Usage Instructions](#usage-instructions)**
    + **[Import](#import)**
    + **[Initialize variables](#initialize-variables)**
    + **[Sync](#sync)**
        1. **[Single Module](#single-module)**
        2. **[Sync All](#sync-all)**
    + **[Add New](#add-new)**
    + **[Edit](#edit)**
    + **[Remove](#remove)**

## Installation Instructions

### PYPI

```bash
pip3 install -U jasmin-telnet
```

### From Source

```bash
git clone https://github.com/BlackOrder/jasmin_telnet.git
cd jasmin_telnet
pip3 install .
```

## Usage Instructions

### Import

```bash
from jasmin_telnet.proxy import Proxy as JasminTelnetProxy
```

### Initialize variables

```python
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

#### Single Module

To sync, remove any sub-module not sent and add not existing and update existing.

```python
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

```python
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

```python
jasmin_proxy.syncAll()
```

or

```python
jasmin_proxy.syncAll(collection_data={})
```

or

```python
jasmin_proxy.syncAll(collection_data=None)
```

This will flush all of Jasmin configurations.

### Add New

```python
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

```python
jasmin_proxy.edit(
    module="user",
    sub_id="uid3",
    options={
                "password": "NEW_PASS"
            }
)
```

### Remove

```python
jasmin_proxy.remove(
    module="user",
    sub_id="uid3"
)
```
