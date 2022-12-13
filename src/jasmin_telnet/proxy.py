from .conn import TelnetConnection
from .filter import Filter as Telnet_Filter
from .group import Group as Telnet_Group
from .httpccm import HTTPCCM as Telnet_HTTPCCM
from .mointerceptor import MOInterceptor as Telnet_MOInterceptor
from .morouter import MORouter as Telnet_MORouter
from .mtinterceptor import MTInterceptor as Telnet_MTInterceptor
from .mtrouter import MTRouter as Telnet_MTRouter
from .smppccm import SMPPCCM as Telnet_SMPPCCM
from .user import User as Telnet_User
import threading

class Proxy:
    def __init__(self, host: str = "127.0.0.1", port: int = 8990, timeout: int = 10, auth: bool = True, username: str = "jcliadmin", password: str = "jclipwd", standard_prompt: str = "jcli : ", interactive_prompt: str = "> ", log_status: bool = False, logger=None):
        """ Constructor """
        self.telnet_host = host
        self.telnet_port = port
        self.telnet_timeout = timeout
        self.telnet_auth = auth
        self.telnet_username = username
        self.telnet_password = password
        self.telnet_standard_prompt = standard_prompt
        self.telnet_interactive_prompt = interactive_prompt
        self.log_status = log_status
        if logger is None:
            self.logger = self.log
        else:
            self.logger = logger


    def getTelnetConn(self) -> TelnetConnection:
        return TelnetConnection(
            host=self.telnet_host,
            port=self.telnet_port,
            timeout=self.telnet_timeout,
            auth=self.telnet_auth,
            username=self.telnet_username,
            password=self.telnet_password,
            standard_prompt=self.telnet_standard_prompt,
            interactive_prompt=self.telnet_interactive_prompt,
        )

    def log(self, log: str):
        """ holder for disabled logger """
        pass

    def syncAll(self, collection_data: dict[str, dict[str, dict[str, str | int | float | bool]]]):
        """ Excute Sync all modules function """
        if not isinstance(collection_data, dict):
            collection_data = {}
        if "smppccm" not in collection_data:
            collection_data["smppccm"] = False
        if "httpccm" not in collection_data:
            collection_data["httpccm"] = False
        if "group" not in collection_data:
            collection_data["group"] = False
        if "filter" not in collection_data:
            collection_data["filter"] = False
        if "mointerceptor" not in collection_data:
            collection_data["mointerceptor"] = False
        if "mtinterceptor" not in collection_data:
            collection_data["mtinterceptor"] = False
        if "user" not in collection_data:
            collection_data["user"] = False
        if "morouter" not in collection_data:
            collection_data["morouter"] = False
        if "mtrouter" not in collection_data:
            collection_data["mtrouter"] = False
        self.syncCollection(collection_data)

    def syncCollection(self, collection_data: dict[str, dict[str, dict[str, str | int | float | bool]]]):
        """ Excute Sync a collection of modules with threads function """
        jobs_levels: list[list[threading.Thread], list[threading.Thread], list[threading.Thread],
                          list[threading.Thread], list[threading.Thread]] = [[], [], [], [], []]

        if "group" in collection_data:
            jobs_levels[0].append(threading.Thread(target=self.syncOneFromCollection, kwargs={
                "collection_data": collection_data,
                "module": "group",
            }))
        if "smppccm" in collection_data:
            jobs_levels[0].append(threading.Thread(target=self.syncOneFromCollection, kwargs={
                "collection_data": collection_data,
                "module": "smppccm",
            }))
        if "httpccm" in collection_data:
            jobs_levels[0].append(threading.Thread(target=self.syncOneFromCollection, kwargs={
                "collection_data": collection_data,
                "module": "httpccm",
            }))
        if "user" in collection_data:
            jobs_levels[1].append(threading.Thread(target=self.syncOneFromCollection, kwargs={
                "collection_data": collection_data,
                "module": "user",
            }))
        if "filter" in collection_data:
            jobs_levels[2].append(threading.Thread(target=self.syncOneFromCollection, kwargs={
                "collection_data": collection_data,
                "module": "filter",
            }))
        if "mointerceptor" in collection_data:
            jobs_levels[3].append(threading.Thread(target=self.syncOneFromCollection, kwargs={
                "collection_data": collection_data,
                "module": "mointerceptor",
            }))
        if "mtinterceptor" in collection_data:
            jobs_levels[3].append(threading.Thread(target=self.syncOneFromCollection, kwargs={
                "collection_data": collection_data,
                "module": "mtinterceptor",
            }))
        if "morouter" in collection_data:
            jobs_levels[4].append(threading.Thread(target=self.syncOneFromCollection, kwargs={
                "collection_data": collection_data,
                "module": "morouter",
            }))
        if "mtrouter" in collection_data:
            jobs_levels[4].append(threading.Thread(target=self.syncOneFromCollection, kwargs={
                "collection_data": collection_data,
                "module": "mtrouter",
            }))

        # Loop all jobs levels
        for jobs_level in jobs_levels:
            # Start all jobs in this level
            for job in jobs_level:
                job.start()
            # Wait for all jobs in this level to finish
            for job in jobs_level:
                try:
                    job.join()
                except KeyboardInterrupt:
                    pass
        del jobs_levels

    def syncOneFromCollection(self, module: str, collection_data: dict[str, dict[str, dict[str, str | int | float | bool]]]):
        """ Excute Sync a given module from a collection function """
        self.sync(module=module, sub_modules_data=collection_data[module])

    def sync(self, module: str, sub_modules_data: dict[str, dict[str, str | int | float | bool]]):
        """ Excute Sync a given module function """
        telnet = self.getTelnetConn()

        if module == "smppccm":
            self.logger("          Sync: Smppccm module.")
            Smppccm(telnet_conn=telnet).sync(sub_modules_data=sub_modules_data)
        if module == "httpccm":
            self.logger("          Sync: Httpccm module.")
            Httpccm(telnet_conn=telnet).sync(sub_modules_data=sub_modules_data)
        if module == "group":
            self.logger("          Sync: Group module.")
            Group(telnet_conn=telnet).sync(sub_modules_data=sub_modules_data)
        if module == "user":
            self.logger("          Sync: User module.")
            User(telnet_conn=telnet).sync(sub_modules_data=sub_modules_data)
        if module == "filter":
            self.logger("          Sync: Filter module.")
            Filter(telnet_conn=telnet).sync(sub_modules_data=sub_modules_data)
        if module == "mointerceptor":
            self.logger("          Sync: MoInterceptor module.")
            MOInterceptor(telnet_conn=telnet).sync(
                sub_modules_data=sub_modules_data)
        if module == "morouter":
            self.logger("          Sync: MoRouter module.")
            Morouter(telnet_conn=telnet).sync(
                sub_modules_data=sub_modules_data)
        if module == "mtinterceptor":
            self.logger("          Sync: MtInterceptor module.")
            MTInterceptor(telnet_conn=telnet).sync(
                sub_modules_data=sub_modules_data)
        if module == "mtrouter":
            self.logger("          Sync: MtRouter module.")
            Mtrouter(telnet_conn=telnet).sync(
                sub_modules_data=sub_modules_data)

    def add(self, module: str, sub_id: str, options: dict[str, str | int | float | bool]):
        """ Excute Add to a module function """
        telnet = self.getTelnetConn()

        if module == "smppccm":
            self.logger("          Add new: Smppccm module.")
            Smppccm(telnet_conn=telnet).add(sub_id=sub_id, options=options)
        if module == "httpccm":
            self.logger("          Add new: Httpccm module.")
            Httpccm(telnet_conn=telnet).add(sub_id=sub_id, options=options)
        if module == "group":
            self.logger("          Add new: Group module.")
            Group(telnet_conn=telnet).add(sub_id=sub_id, options=options)
        if module == "user":
            self.logger("          Add new: User module.")
            User(telnet_conn=telnet).add(sub_id=sub_id, options=options)
        if module == "filter":
            self.logger("          Add new: Filter module.")
            Filter(telnet_conn=telnet).add(sub_id=sub_id, options=options)
        if module == "mointerceptor":
            self.logger("          Add new: MoInterceptor module.")
            MOInterceptor(telnet_conn=telnet).add(
                sub_id=sub_id, options=options)
        if module == "morouter":
            self.logger("          Add new: MoRouter module.")
            Morouter(telnet_conn=telnet).add(sub_id=sub_id, options=options)
        if module == "mtinterceptor":
            self.logger("          Add new: MtInterceptor module.")
            MTInterceptor(telnet_conn=telnet).add(
                sub_id=sub_id, options=options)
        if module == "mtrouter":
            self.logger("          Add new: MtRouter module.")
            Mtrouter(telnet_conn=telnet).add(sub_id=sub_id, options=options)

    def edit(self, module: str, sub_id: str, options: dict[str, str | int | float | bool]):
        """ Excute Edit a module function """
        telnet = self.getTelnetConn()

        if module == "smppccm":
            self.logger("          Update: Smppccm module.")
            Smppccm(telnet_conn=telnet).update(sub_id=sub_id, options=options)
        if module == "httpccm":
            self.logger("          Update: Httpccm module.")
            Httpccm(telnet_conn=telnet).update(sub_id=sub_id, options=options)
        if module == "group":
            self.logger("          Update: Group module.")
            Group(telnet_conn=telnet).update(sub_id=sub_id, options=options)
        if module == "user":
            self.logger("          Update: User module.")
            User(telnet_conn=telnet).update(sub_id=sub_id, options=options)
        if module == "filter":
            self.logger("          Update: Filter module.")
            Filter(telnet_conn=telnet).update(sub_id=sub_id, options=options)
        if module == "mointerceptor":
            self.logger("          Update: MoInterceptor module.")
            MOInterceptor(telnet_conn=telnet).update(
                sub_id=sub_id, options=options)
        if module == "morouter":
            self.logger("          Update: MoRouter module.")
            Morouter(telnet_conn=telnet).update(sub_id=sub_id, options=options)
        if module == "mtinterceptor":
            self.logger("          Update: MtInterceptor module.")
            MTInterceptor(telnet_conn=telnet).update(
                sub_id=sub_id, options=options)
        if module == "mtrouter":
            self.logger("          Update: MtRouter module.")
            Mtrouter(telnet_conn=telnet).update(sub_id=sub_id, options=options)

    def remove(self, module: str, sub_id: str):
        """ Excute Remove from a module function """
        telnet = self.getTelnetConn()

        if module == "smppccm":
            self.logger("          Remove: Smppccm module.")
            Smppccm(telnet_conn=telnet).remove(sub_id=sub_id)
        if module == "httpccm":
            self.logger("          Remove: Httpccm module.")
            Httpccm(telnet_conn=telnet).remove(sub_id=sub_id)
        if module == "group":
            self.logger("          Remove: Group module.")
            Group(telnet_conn=telnet).remove(sub_id=sub_id)
        if module == "user":
            self.logger("          Remove: User module.")
            User(telnet_conn=telnet).remove(sub_id=sub_id)
        if module == "filter":
            self.logger("          Remove: Filter module.")
            Filter(telnet_conn=telnet).remove(sub_id=sub_id)
        if module == "mointerceptor":
            self.logger("          Remove: MoInterceptor module.")
            MOInterceptor(telnet_conn=telnet).remove(sub_id=sub_id)
        if module == "morouter":
            self.logger("          Remove: MoRouter module.")
            Morouter(telnet_conn=telnet).remove(sub_id=sub_id)
        if module == "mtinterceptor":
            self.logger("          Remove: MtInterceptor module.")
            MTInterceptor(telnet_conn=telnet).remove(sub_id=sub_id)
        if module == "mtrouter":
            self.logger("          Remove: MtRouter module.")
            Mtrouter(telnet_conn=telnet).remove(sub_id=sub_id)


class Filter:
    def __init__(self, telnet_conn: TelnetConnection):
        self.manager = Telnet_Filter(conn=telnet_conn)

    def sync(self, sub_modules_data: dict[str, dict[str, str | int | float | bool]]):
        synced_ids: list[str] = []
        manager_ids: list[str] = [sub_status[self.manager.statusHeaderID]
                                  for sub_status in self.manager.listStatus()]
        for sub_id, options in sub_modules_data.items():
            synced_ids.append(sub_id)
            if sub_id in manager_ids:
                self.update(sub_id=sub_id, options=options)
            else:
                self.add(sub_id=sub_id, options=options)
                manager_ids.append(sub_id)

        for manager_id in manager_ids:
            if manager_id not in synced_ids:
                self.remove(sub_id=manager_id)

    def add(self, sub_id: str, options: dict[str, str | int | float | bool]):
        self.manager.create(data=options)

    def update(self, sub_id: str, options: dict[str, str | int | float | bool]):
        self.add(sub_id=sub_id, options=options)

    def remove(self, sub_id):
        self.manager.destroy(sub_id=sub_id)


class Group:
    def __init__(self, telnet_conn: TelnetConnection):
        self.manager = Telnet_Group(conn=telnet_conn)

    def sync(self, sub_modules_data: dict[str, dict[str, str | int | float | bool]]):
        synced_ids: list[str] = []
        manager_ids: list[str] = [sub_status[self.manager.statusHeaderID]
                                  for sub_status in self.manager.listStatus()]
        for sub_id, options in sub_modules_data.items():
            synced_ids.append(sub_id)
            if sub_id in manager_ids:
                self.update(sub_id=sub_id, options=options)
            else:
                self.add(sub_id=sub_id, options=options)
                manager_ids.append(sub_id)

        for manager_id in manager_ids:
            if manager_id not in synced_ids:
                self.remove(sub_id=manager_id)

    def add(self, sub_id: str, options: dict[str, str | int | float | bool]):
        processed_data = {key: options[key] for key in set(
            list(options.keys())) - set(["status"])}
        self.manager.create(data=processed_data)
        if "status" in options.keys():
            if options["status"]:
                self.manager.enable(sub_id=sub_id)
            else:
                self.manager.disable(sub_id=sub_id)

    def update(self, sub_id: str, options: dict[str, str | int | float | bool]):
        self.add(sub_id=sub_id, options=options)

    def remove(self, sub_id):
        self.manager.destroy(sub_id=sub_id)


class Httpccm:
    def __init__(self, telnet_conn: TelnetConnection):
        self.manager = Telnet_HTTPCCM(conn=telnet_conn)

    def sync(self, sub_modules_data: dict[str, dict[str, str | int | float | bool]]):
        synced_ids: list[str] = []
        manager_ids: list[str] = [sub_status[self.manager.statusHeaderID]
                                  for sub_status in self.manager.listStatus()]
        for sub_id, options in sub_modules_data.items():
            synced_ids.append(sub_id)
            if sub_id in manager_ids:
                self.update(sub_id=sub_id, options=options)
            else:
                self.add(sub_id=sub_id, options=options)
                manager_ids.append(sub_id)

        for manager_id in manager_ids:
            if manager_id not in synced_ids:
                self.remove(sub_id=manager_id)

    def add(self, sub_id: str, options: dict[str, str | int | float | bool]):
        self.manager.create(data=options)

    def update(self, sub_id: str, options: dict[str, str | int | float | bool]):
        self.add(sub_id=sub_id, options=options)

    def remove(self, sub_id):
        self.manager.destroy(sub_id=sub_id)


class MOInterceptor:
    def __init__(self, telnet_conn: TelnetConnection):
        self.manager = Telnet_MOInterceptor(conn=telnet_conn)

    def sync(self, sub_modules_data: dict[str, dict[str, str | int | float | bool]]):
        synced_ids: list[str] = []
        manager_ids: list[str] = [sub_status[self.manager.statusHeaderID]
                                  for sub_status in self.manager.listStatus()]
        for sub_id, options in sub_modules_data.items():
            synced_ids.append(sub_id)
            if sub_id in manager_ids:
                self.update(sub_id=sub_id, options=options)
            else:
                self.add(sub_id=sub_id, options=options)
                manager_ids.append(sub_id)

        for manager_id in manager_ids:
            if manager_id not in synced_ids:
                self.remove(sub_id=manager_id)

    def add(self, sub_id: str, options: dict[str, str | int | float | bool]):
        self.manager.create(data=options)

    def update(self, sub_id: str, options: dict[str, str | int | float | bool]):
        self.add(sub_id=sub_id, options=options)

    def remove(self, sub_id):
        self.manager.destroy(sub_id=sub_id)


class Morouter:
    def __init__(self, telnet_conn: TelnetConnection):
        self.manager = Telnet_MORouter(conn=telnet_conn)

    def sync(self, sub_modules_data: dict[str, dict[str, str | int | float | bool]]):
        synced_ids: list[str] = []
        manager_ids: list[str] = [sub_status[self.manager.statusHeaderID]
                                  for sub_status in self.manager.listStatus()]
        for sub_id, options in sub_modules_data.items():
            synced_ids.append(sub_id)
            if sub_id in manager_ids:
                self.update(sub_id=sub_id, options=options)
            else:
                self.add(sub_id=sub_id, options=options)
                manager_ids.append(sub_id)

        for manager_id in manager_ids:
            if manager_id not in synced_ids:
                self.remove(sub_id=manager_id)

    def add(self, sub_id: str, options: dict[str, str | int | float | bool]):
        self.manager.create(data=options)

    def update(self, sub_id: str, options: dict[str, str | int | float | bool]):
        self.add(sub_id=sub_id, options=options)

    def remove(self, sub_id):
        self.manager.destroy(sub_id=sub_id)


class MTInterceptor:
    def __init__(self, telnet_conn: TelnetConnection):
        self.manager = Telnet_MTInterceptor(conn=telnet_conn)

    def sync(self, sub_modules_data: dict[str, dict[str, str | int | float | bool]]):
        synced_ids: list[str] = []
        manager_ids: list[str] = [sub_status[self.manager.statusHeaderID]
                                  for sub_status in self.manager.listStatus()]
        for sub_id, options in sub_modules_data.items():
            synced_ids.append(sub_id)
            if sub_id in manager_ids:
                self.update(sub_id=sub_id, options=options)
            else:
                self.add(sub_id=sub_id, options=options)
                manager_ids.append(sub_id)

        for manager_id in manager_ids:
            if manager_id not in synced_ids:
                self.remove(sub_id=manager_id)

    def add(self, sub_id: str, options: dict[str, str | int | float | bool]):
        self.manager.create(data=options)

    def update(self, sub_id: str, options: dict[str, str | int | float | bool]):
        self.add(sub_id=sub_id, options=options)

    def remove(self, sub_id):
        self.manager.destroy(sub_id=sub_id)


class Mtrouter:
    def __init__(self, telnet_conn: TelnetConnection):
        self.manager = Telnet_MTRouter(conn=telnet_conn)

    def sync(self, sub_modules_data: dict[str, dict[str, str | int | float | bool]]):
        synced_ids: list[str] = []
        manager_ids: list[str] = [sub_status[self.manager.statusHeaderID]
                                  for sub_status in self.manager.listStatus()]
        for sub_id, options in sub_modules_data.items():
            synced_ids.append(sub_id)
            if sub_id in manager_ids:
                self.update(sub_id=sub_id, options=options)
            else:
                self.add(sub_id=sub_id, options=options)
                manager_ids.append(sub_id)

        for manager_id in manager_ids:
            if manager_id not in synced_ids:
                self.remove(sub_id=manager_id)

    def add(self, sub_id: str, options: dict[str, str | int | float | bool]):
        self.manager.create(data=options)

    def update(self, sub_id: str, options: dict[str, str | int | float | bool]):
        self.add(sub_id=sub_id, options=options)

    def remove(self, sub_id):
        self.manager.destroy(sub_id=sub_id)


class Smppccm:
    def __init__(self, telnet_conn: TelnetConnection):
        self.manager = Telnet_SMPPCCM(conn=telnet_conn)

    def sync(self, sub_modules_data: dict[str, dict[str, str | int | float | bool]]):
        synced_ids: list[str] = []
        manager_ids: list[str] = [sub_status[self.manager.statusHeaderID]
                                  for sub_status in self.manager.listStatus()]
        for sub_id, options in sub_modules_data.items():
            synced_ids.append(sub_id)
            if sub_id in manager_ids:
                self.update(sub_id=sub_id, options=options)
            else:
                self.add(sub_id=sub_id, options=options)
                manager_ids.append(sub_id)

        for manager_id in manager_ids:
            if manager_id not in synced_ids:
                self.remove(sub_id=manager_id)

    def add(self, sub_id: str, options: dict[str, str | int | float | bool]):
        processed_data = {key: options[key] for key in set(
            list(options.keys())) - set(["status"])}
        self.manager.create(data=processed_data)
        if "status" in options.keys():
            if options["status"]:
                self.manager.start(sub_id=sub_id)
            else:
                self.manager.stop(sub_id=sub_id)

    def update(self, sub_id: str, options: dict[str, str | int | float | bool]):
        processed_data = {key: options[key] for key in set(
            list(options.keys())) - set(["status"])}
        self.manager.partial_update(data=processed_data, sub_id=sub_id)
        if "status" in options.keys():
            if options["status"]:
                self.manager.start(sub_id=sub_id)
            else:
                self.manager.stop(sub_id=sub_id)

    def remove(self, sub_id):
        self.manager.destroy(sub_id=sub_id)


class User:
    def __init__(self, telnet_conn: TelnetConnection):
        self.manager = Telnet_User(conn=telnet_conn)

    def sync(self, sub_modules_data: dict[str, dict[str, str | int | float | bool]]):
        synced_ids: list[str] = []
        manager_ids: list[str] = [sub_status[self.manager.statusHeaderID]
                                  for sub_status in self.manager.listStatus()]
        for sub_id, options in sub_modules_data.items():
            synced_ids.append(sub_id)
            if sub_id in manager_ids:
                self.update(sub_id=sub_id, options=options)
            else:
                self.add(sub_id=sub_id, options=options)
                manager_ids.append(sub_id)

        for manager_id in manager_ids:
            if manager_id not in synced_ids:
                self.remove(sub_id=manager_id)

    def add(self, sub_id: str, options: dict[str, str | int | float | bool]):
        processed_data = {key: options[key] for key in set(
            list(options.keys())) - set(["status"])}
        self.manager.create(data=processed_data)
        if "status" in options.keys():
            if options["status"]:
                self.manager.enable(sub_id=sub_id)
            else:
                self.manager.disable(sub_id=sub_id)

    def update(self, sub_id: str, options: dict[str, str | int | float | bool]):
        processed_data = {key: options[key] for key in set(
            list(options.keys())) - set(["status"])}
        self.manager.partial_update(data=processed_data, sub_id=sub_id)
        if "status" in options.keys():
            if options["status"]:
                self.manager.enable(sub_id=sub_id)
            else:
                self.manager.disable(sub_id=sub_id)

    def remove(self, sub_id):
        self.manager.destroy(sub_id=sub_id)
