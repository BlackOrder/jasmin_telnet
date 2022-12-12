from .conn import TelnetConnection
from .basicmanager import BasicManager, ObjectNotFoundError


class Group(BasicManager):
    "Users for managing *Jasmin* users"

    def __init__(self, conn: TelnetConnection):
        super().__init__(conn=conn, module="group", lookup_field="gid")
        self.statusHeaderID = "Group id"

    def _parseSingleStatus(self, status_list: list) -> dict[str, str | int | float | bool]:
        """ Groups for managing *Jasmin* user groups (*not* Django auth groups) """
        return {
            self.statusHeaderID: status_list[0].lstrip("!"),
            "status": not status_list[0][0] == "!"
        }

    def get_one(self, sub_id: str) -> dict[str, str | int | float | bool]:
        """Gets a single SubModule data """
        allSubModulesStatus = self.allSubModulesStatus if hasattr(
            self, "allSubModulesStatus") else self.listStatus()
        if not any(d[self.statusHeaderID] == sub_id for d in allSubModulesStatus):
            raise ObjectNotFoundError(f"Unknown {self.module}: {sub_id}")
        return [u for u in allSubModulesStatus if u[self.statusHeaderID] == sub_id][0]

    def enable(self, sub_id: str) -> bool | str:
        """Enable a group. One parameter required, the group identifier (a string)
        """
        return self._simple_submodule_action(action="e", sub_id=sub_id)

    def disable(self, sub_id: str) -> bool | str:
        """Disable a group. One parameter required, the group identifier (a string)
        """
        return self._simple_submodule_action(action="d", sub_id=sub_id)

    def _getRequiredAttributes(self, data: dict) -> list[str]:
        """ Required for create, can use data:dict to check if some keys depends on others """
        prioritAttributes = self._getPrioritAttributes()
        requiredAttributes = []
        return prioritAttributes + list(set(requiredAttributes) - set(prioritAttributes))

    def _getPrioritAttributes(self) -> list[str]:
        """ Always sent first """
        return ["gid"]

    def _getGuardedAttributes(self) -> list[str]:
        """ NEVER send for Update """
        return ["gid"]
