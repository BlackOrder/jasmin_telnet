from .conn import TelnetConnection
from .exceptions import (CanNotModifyError,
                         JasminSyntaxError, JasminError,
                         UnknownError, MissingKeyError,
                         ObjectNotFoundError)


class BasicManager(object):
    "Basic Manager for managing *Jasmin*"

    def __init__(self, conn: TelnetConnection, module: str, lookup_field: str, defaultPersist: bool = True):
        self.conn = conn
        self.telnet = conn.telnet
        self.STANDARD_PROMPT = conn.STANDARD_PROMPT
        self.INTERACTIVE_PROMPT = conn.INTERACTIVE_PROMPT
        self.module = module
        self.lookup_field = lookup_field
        self.defaultPersist = defaultPersist

    def create(self, data: dict[str, str | int | float | bool]) -> bool:
        """Create a SubModule.
        """
        if set(self._getRequiredAttributes(data=data)) > set(data):
            raise MissingKeyError(
                f"Missing parameter: {self._getRequiredAttributes(data=data)} required")

        data = self._prepareAttributes(data)
        self.telnet.sendline(f"{self.module} -a")
        self.telnet.expect(r"Adding a new (.+)\n" +
                           self.INTERACTIVE_PROMPT)
        self._set_ikeys(
            keys2vals=data, priorityKeys=self._getPrioritAttributes())
        self._persist()
        return True

    def listAll(self) -> list[dict[str, str | int | float | bool]]:
        "List SubModules. No parameters"
        self.telnet.sendline(f"{self.module} -l")
        self.telnet.expect([r"(.+)\n" + self.STANDARD_PROMPT])
        result = self.telnet.match.group(0).strip()
        if len(result) < 3:
            return []

        results = [l for l in result.splitlines() if l]

        self.allSubModulesStatus: list[dict] = [self._parseSingleStatus(status_list=str(
            u, "utf-8").lstrip("#").lstrip().split(None)) for u in results[2:-2]]

        sub_modules = [self.get_one(sub_id=str(u, "utf-8").lstrip("#").lstrip().split(None, 1)[0].lstrip("!"))
                       for u in results[2:-2]]
        delattr(self, "allSubModulesStatus")
        return [
            # return sub_modules skipping None (== nonexistent sub_module)
            sub_module for sub_module in sub_modules if sub_modules
        ]

    def listStatus(self) -> list[dict[str, str | int | float | bool]]:
        "List SubModules Status. No parameters"
        self.telnet.sendline(f"{self.module} -l")
        self.telnet.expect([r"(.+)\n" + self.STANDARD_PROMPT])
        result = self.telnet.match.group(0).strip()
        if len(result) < 3:
            return []

        results = [l for l in result.splitlines() if l]

        status_list = [self._parseSingleStatus(status_list=str(
            u, "utf-8").lstrip("#").lstrip().split(None)) for u in results[2:-2]]
        return [
            # return SubModules skipping None (== nonexistent SubModule)
            sub_module_status for sub_module_status in status_list if sub_module_status
        ]

    def get_one(self, sub_id: str) -> dict[str, str | int | float | bool]:
        """Gets a single SubModule data """
        self.telnet.sendline(f"{self.module} -s {sub_id}")
        matched_index = self.telnet.expect([
            r".+Unknown .+:.*" + self.STANDARD_PROMPT,
            r".+Usage: .+.*" + self.STANDARD_PROMPT,
            r"(.+)\n" + self.STANDARD_PROMPT,
        ])
        if matched_index != 2:
            raise ObjectNotFoundError(f"Unknown {self.module}: {sub_id}")
        result = self.telnet.match.group(1)
        sub_module = {}
        for line in [l for l in result.splitlines() if l][1:]:
            d = [str(x, "utf-8") for x in line.split() if x]
            sub_module[" ".join(d[:-1] if len(d) > 1 else d)
                       ] = d[-1] if len(d) > 1 else None
        return self._parseSingle(sub_module=sub_module)

    def destroy(self, sub_id: str):
        """Delete a SubModule. One parameter required, the SubModule identifier (a string)
        """
        return self._simple_submodule_action("r", sub_id)

    def _simple_submodule_action(self, action: str, sub_id: str) -> bool | str:
        self.telnet.sendline(f"{self.module} -{action} {sub_id}")
        matched_index = self.telnet.expect([
            r".+Successfully(.+)" + self.STANDARD_PROMPT,
            r".+Unknown .+: (.+)" + self.STANDARD_PROMPT,
            r".+(.*)" + self.STANDARD_PROMPT,
        ])
        if matched_index == 0:
            self._persist()
            return True
        elif matched_index == 1:
            raise ObjectNotFoundError(f"Unknown {self.module}: {sub_id}")
        else:
            return self.telnet.match.group(0).strip()

    def _parseSingleStatus(self, status_list: list) -> dict[str, str | int | float | bool]:
        """ Holder, each subClass should override """
        return {idx: x for idx, x in enumerate(status_list)}

    def _parseSingle(self, sub_module: dict[str, str | int | float | bool]) -> dict[str, str | int | float | bool]:
        """ Holder, each subClass should override """
        return sub_module

    def _prepareAttributes(self, data: dict[str, str | int | float | bool]) -> dict[str, str | int | float | bool]:
        """ If data needs preparing """
        return data

    def _getRequiredAttributes(self, data: dict[str, str | int | float | bool]) -> list[str]:
        """ Required for create, can use data:dict to check if some keys depends on others """
        return []

    def _getPrioritAttributes(self) -> list[str]:
        """ Always sent first """
        return []

    def _getGuardedAttributes(self) -> list[str]:
        """ NEVER Update """
        return []

    def _persist(self) -> None:
        if self.defaultPersist:
            self.telnet.sendline("persist\n")
            self.telnet.expect(r".*" + self.STANDARD_PROMPT)

    def _set_ikeys(self, keys2vals: dict, priorityKeys: list = []):
        "set multiple keys for interactive command"
        if len(priorityKeys) > 0:
            # Priority Keys first if set
            for key, val in keys2vals.items():
                if key in priorityKeys:
                    self._send_key_val(key=key, val=val)
        for key, val in keys2vals.items():
            # if priority, skip. already sent
            if key not in priorityKeys:
                self._send_key_val(key=key, val=val)
        self.telnet.sendline("ok")
        ok_index = self.telnet.expect([
            r"ok(.* syntax is invalid).*" + self.INTERACTIVE_PROMPT,
            r".*" + self.STANDARD_PROMPT,
        ])
        if ok_index == 0:
            # remove whitespace and return error
            raise JasminSyntaxError(
                " ".join(self.telnet.match.group(1).split()))
        return

    def _send_key_val(self, key: str, val: str):
        self.telnet.sendline("%s %s" % (key, val))
        matched_index = self.telnet.expect([
            r".*(Unknown .*)" + self.INTERACTIVE_PROMPT,
            r"(.*) can not be modified.*" + self.INTERACTIVE_PROMPT,
            r"(.*)" + self.INTERACTIVE_PROMPT
        ])
        result = self.telnet.match.group(1).strip()
        if matched_index == 0:
            raise UnknownError(result)
        if matched_index == 1:
            raise CanNotModifyError(result)

    def _split_dict_cols(self, keys2vals: dict[str, str | int | float | bool]) -> list[list[str]]:
        "split columns into lists"
        parsed = []
        for key, value in keys2vals.items():
            fields: list = key.split()
            fields.append(str(value))
            parsed.append(fields)
        return parsed
