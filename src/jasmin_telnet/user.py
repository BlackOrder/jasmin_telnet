from jasmin_telnet.basicmanager import (BasicManager, JasminSyntaxError,
                                        UnknownError)
from jasmin_telnet.conn import TelnetConnection


class User(BasicManager):
    "Users for managing *Jasmin* users"

    def __init__(self, conn: TelnetConnection):
        super().__init__(conn=conn, module="user", lookup_field="uid")
        self.statusHeaderID = "User id"

    def partial_update(self, data: dict[str, str | int | float | bool], sub_id: str) -> bool:
        """Update some SubModule attributes
        """
        if not ((type(data) is dict) and (len(data) >= 1)):
            raise JasminSyntaxError("updates should be a dict")

        processed_data = self._split_dict_cols(data)
        data = [x for x in processed_data if x[0]
                not in self._getGuardedAttributes()]

        if not ((type(data) is list) and (len(data) >= 1)):
            raise JasminSyntaxError(
                "updates should contains some keys which can be updated")

        self.telnet.sendline(f"{self.module} -u {sub_id}")
        matched_index = self.telnet.expect([
            r".*Updating (.*)" + self.INTERACTIVE_PROMPT,
            r".*Unknown .+: (.*)" + self.STANDARD_PROMPT,
            r".+(.*)(" + self.INTERACTIVE_PROMPT +
            "|" + self.STANDARD_PROMPT + ")",
        ])
        if matched_index == 1:
            raise UnknownError(f"Unknown {self.module}: {sub_id}")
        if matched_index != 0:
            raise UnknownError(self.telnet.match.group(0))
        for update in data:
            if not ((type(update) is list) and (len(update) >= 1)):
                raise JasminSyntaxError("Not a list: %s" % update)
            self.telnet.sendline(" ".join([x for x in update]))
            matched_index = self.telnet.expect([
                r".*(Unknown .+ key:.*)" + self.INTERACTIVE_PROMPT,
                r".*(Error:.*)" + self.STANDARD_PROMPT,
                r".*" + self.INTERACTIVE_PROMPT,
                r".+(.*)(" + self.INTERACTIVE_PROMPT +
                "|" + self.STANDARD_PROMPT + ")",
            ])
            if matched_index != 2:
                raise JasminSyntaxError(
                    " ".join(self.telnet.match.group(1).split()))
        self.telnet.sendline("ok")
        ok_index = self.telnet.expect([
            r"(.*)" + self.INTERACTIVE_PROMPT,
            r".*" + self.STANDARD_PROMPT,
        ])
        if ok_index == 0:
            raise JasminSyntaxError(
                " ".join(self.telnet.match.group(1).split()))
        self._persist()
        return True

    def _parseSingleStatus(self, status_list: list) -> dict[str, str | int | float | bool]:
        """ Holder, each subClass should override """
        return {
            self.statusHeaderID: status_list[0].lstrip("!"),
            "Group id": status_list[1].lstrip("!"),
            "Username": status_list[2],
            "Balance MT": status_list[3],
            "Balance SMS": status_list[4],
            "Throughput": status_list[5],
            "status": not status_list[0][0] == "!" and not status_list[1][0] == "!"
        }

    def _parseSingle(self, sub_module: dict[str, str | int | float | bool]) -> dict[str, str | int | float | bool]:
        """ Holder, each subClass should override """
        allSubModulesStatus = self.allSubModulesStatus if hasattr(
            self, "allSubModulesStatus") else self.listStatus()
        if not any(d[self.statusHeaderID] == sub_module[self.lookup_field] for d in allSubModulesStatus):
            sub_module["status"] = False
            return sub_module
        userStatus = [u for u in allSubModulesStatus if u[self.statusHeaderID]
                      == sub_module[self.lookup_field]][0]
        sub_module["status"] = userStatus["status"]
        return sub_module

    def enable(self, sub_id: str) -> bool | str:
        """Enable a user. One parameter required, the user identifier (a string)
        """
        return self._simple_submodule_action(action="e", sub_id=sub_id)

    def disable(self, sub_id: str) -> bool | str:
        """Disable a user. One parameter required, the user identifier (a string)
        """
        return self._simple_submodule_action(action="d", sub_id=sub_id)

    def smpp_unbind(self, sub_id: str) -> bool | str:
        """Unbind user from smpp server
        """
        return self._simple_submodule_action(action="-smpp-unbind", sub_id=sub_id)

    def smpp_ban(self, sub_id: str) -> bool | str:
        """Unbind and ban user from smpp server
        """
        return self._simple_submodule_action(action="-smpp-ban", sub_id=sub_id)

    def _getRequiredAttributes(self, data: dict[str, str | int | float | bool]) -> list[str]:
        """ Required for create, can use data:dict to check if some keys depends on others """
        prioritAttributes = self._getPrioritAttributes()
        requiredAttributes = ["username", "password"]
        return prioritAttributes + list(set(requiredAttributes) - set(prioritAttributes))

    def _getPrioritAttributes(self) -> list[str]:
        """ Always sent first """
        return ["uid", "gid"]

    def _getGuardedAttributes(self) -> list[str]:
        """ NEVER send for Update """
        return ["username", "uid"]
