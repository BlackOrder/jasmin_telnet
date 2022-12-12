from .conn import TelnetConnection
from .basicmanager import BasicManager, ObjectNotFoundError


class HTTPCCM(BasicManager):
    "HTTPCCM for managing HTTP Client Connectors"

    def __init__(self, conn: TelnetConnection):
        super().__init__(conn=conn, module="httpccm", lookup_field="cid")
        self.statusHeaderID = "Httpcc id"

    def _parseSingleStatus(self, status_list: list) -> dict[str, str | int | float | bool]:
        """ Holder, each subClass should override """
        return {
            self.statusHeaderID: status_list[0],
            "Type": status_list[1],
            "Method": status_list[2],
            "URL": status_list[3]
        }

    def get_one(self, sub_id: str) -> dict[str, str | int | float | bool]:
        """Gets a single SubModule data """
        allSubModulesStatus = self.allSubModulesStatus if hasattr(
            self, "allSubModulesStatus") else self.listStatus()
        if not any(d[self.statusHeaderID] == sub_id for d in allSubModulesStatus):
            raise ObjectNotFoundError(f"Unknown {self.module}: {sub_id}")
        return [u for u in allSubModulesStatus if u[self.statusHeaderID] == sub_id][0]

    def _getRequiredAttributes(self, data: dict[str, str | int | float | bool]) -> list[str]:
        """ Required for create, can use data:dict to check if some keys depends on others """
        prioritAttributes = self._getPrioritAttributes()
        requiredAttributes = ["url", "method"]
        return prioritAttributes + list(set(requiredAttributes) - set(prioritAttributes))

    def _getPrioritAttributes(self) -> list[str]:
        """ Always sent first """
        return ["cid"]

    def _getGuardedAttributes(self) -> list[str]:
        """ NEVER send for Update """
        return ["cid"]
