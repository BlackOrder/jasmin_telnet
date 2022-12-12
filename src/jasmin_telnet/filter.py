from .conn import TelnetConnection
from .basicmanager import BasicManager, ObjectNotFoundError


class Filter(BasicManager):
    "Filters Class"

    def __init__(self, conn: TelnetConnection):
        super().__init__(conn=conn, module="filter", lookup_field="fid")
        self.statusHeaderID = "Filter id"

    def _parseSingleStatus(self, status_list: list) -> dict[str, str | int | float | bool]:
        """ Holder, each subClass should override """
        return {
            self.statusHeaderID: status_list[0],
            "Type": status_list[1],
            "Routes": status_list[2] + " " + status_list[3],
            "Description": " ".join(status_list[4:])
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
        requiredAttributes = ["fid"]
        if "type" not in data or data["type"].lower() == "transparentfilter":
            pass

        elif data["type"].lower() == "connectorfilter":
            requiredAttributes.extend(["cid"])

        elif data["type"].lower() == "userfilter":
            requiredAttributes.extend(["uid"])

        elif data["type"].lower() == "groupfilter":
            requiredAttributes.extend(["gid"])

        elif data["type"].lower() == "sourceaddrfilter":
            requiredAttributes.extend(["source_addr"])

        elif data["type"].lower() == "destinationaddrfilter":
            requiredAttributes.extend(["destination_addr"])

        elif data["type"].lower() == "shortmessagefilter":
            requiredAttributes.extend(["short_message"])

        elif data["type"].lower() == "dateintervalfilter":
            requiredAttributes.extend(["dateInterval"])

        elif data["type"].lower() == "timeintervalfilter":
            requiredAttributes.extend(["timeInterval"])

        elif data["type"].lower() == "tagfilter":
            requiredAttributes.extend(["tag"])

        elif data["type"].lower() == "evalpyfilter":
            requiredAttributes.extend(["pyCode"])

        return prioritAttributes + list(set(requiredAttributes) - set(prioritAttributes))

    def _getPrioritAttributes(self) -> list[str]:
        """ Always sent first """
        return ["type"]

    def _getGuardedAttributes(self) -> list[str]:
        """ NEVER send for Update """
        return ["fid"]
