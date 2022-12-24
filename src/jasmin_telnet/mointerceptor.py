import re

from .basicmanager import BasicManager, ObjectNotFoundError
from .conn import TelnetConnection


class MOInterceptor(BasicManager):
    "MOInterceptor for managing MO Interceptors"

    def __init__(self, conn: TelnetConnection):
        super().__init__(conn=conn, module="mointerceptor", lookup_field="order")
        self.statusHeaderID = "Order"

    def _parseSingleStatus(self, status_list: list) -> dict[str, str | int | float | bool]:
        """ Holder, each subClass should override """
        return {
            self.statusHeaderID: status_list[0],
            "Type": status_list[1],
            "Script": re.findall("<MOIS.*?>", " ".join(status_list)),
            "Filter(s)": re.findall("<(?!MOIS).*?>", " ".join(status_list))
        }

    def get_one(self, sub_id: str) -> dict[str, str | int | float | bool]:
        """Gets a single SubModule data """
        allSubModulesStatus = self.allSubModulesStatus if hasattr(
            self, "allSubModulesStatus") else self.listStatus()
        if not any(d[self.statusHeaderID] == sub_id for d in allSubModulesStatus):
            raise ObjectNotFoundError(f"Unknown {self.module}: {sub_id}")
        return [u for u in allSubModulesStatus if u[self.statusHeaderID] == sub_id][0]

    def flush(self) -> bool | str:
        "Flush entire MOInterceptor table"
        self._simple_submodule_action(action="f", sub_id="")

    def _getRequiredAttributes(self, data: dict[str, str | int | float | bool]) -> list[str]:
        """ Required for create, can use data:dict to check if some keys depends on others """
        prioritAttributes = self._getPrioritAttributes()
        requiredAttributes = []
        if "type" not in data:
            pass

        elif data["type"].lower() == "staticmointerceptor":
            requiredAttributes.extend(["filters", "script", "order"])

        elif data["type"].lower() == "defaultinterceptor":
            requiredAttributes.extend(["script"])

        return prioritAttributes + list(set(requiredAttributes) - set(prioritAttributes))

    def _getPrioritAttributes(self) -> list[str]:
        """ Always sent first """
        return ["type"]

    def _getGuardedAttributes(self) -> list[str]:
        """ NEVER send for Update """
        return ["order"]
