from .conn import TelnetConnection
from .basicmanager import BasicManager, JasminSyntaxError, UnknownError


class SMPPCCM(BasicManager):
    "SMPPCCM for managing SMPP Client Connectors"

    def __init__(self, conn: TelnetConnection):
        super().__init__(conn=conn, module="smppccm", lookup_field="cid")
        self.statusHeaderID = "Connector id"

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
            print(self.telnet.match.group(0))
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
            self.statusHeaderID: status_list[0],
            "Service": status_list[1],
            "Session": status_list[2],
            "Starts": status_list[3],
            "Stops": status_list[4],
            "status": status_list[3] > status_list[4]
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

    def start(self, sub_id: str) -> bool | str:
        """ Start SMPP Connector """
        return self._simple_submodule_action(action="1", sub_id=sub_id)

    def stop(self, sub_id: str) -> bool | str:
        """ Stop SMPP Connector """
        return self._simple_submodule_action(action="0", sub_id=sub_id)

    def _getRequiredAttributes(self, data: dict[str, str | int | float | bool]) -> list[str]:
        """ Required for create, can use data:dict to check if some keys depends on others """
        prioritAttributes = self._getPrioritAttributes()
        requiredAttributes = []
        return prioritAttributes + list(set(requiredAttributes) - set(prioritAttributes))

    def _getPrioritAttributes(self) -> list[str]:
        """ Always sent first """
        return ["cid"]

    def _getGuardedAttributes(self) -> list[str]:
        """ NEVER send for Update """
        return ["cid"]
