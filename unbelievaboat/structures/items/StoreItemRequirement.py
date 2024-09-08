from typing import Any, Dict, List, Optional, Union

from ...utils.Constants import ItemRequirementMatchType, ItemRequirementType


class StoreItemRequirement:
    def __init__(self, data: Dict[str, Any]) -> None:
        # TODO: Allow user creation
        self.type: ItemRequirementType = ItemRequirementType[data.get("type")]
        if self.type in [ItemRequirementType.ROLE, ItemRequirementType.ITEM]:
            self.match_type: ItemRequirementMatchType = ItemRequirementMatchType[
                data.get("match_type")
            ]
            self.ids: List[int] = data.get("ids", [])
        elif self.type == ItemRequirementType.TOTAL_BALANCE:
            self.balance: Optional[int] = data.get("balance")

    def json(self) -> Dict[str, Optional[Union[str, int, List[str]]]]:
        json = {
            "type": self.type.name,
        }
        if self.type in [ItemRequirementType.ROLE, ItemRequirementType.ITEM]:
            json["match_type"] = self.match_type.name
            json["ids"] = self.ids
        elif self.type == ItemRequirementType.TOTAL_BALANCE:
            json["balance"] = self.balance
        return json

    def __str__(self) -> str:
        if hasattr(self, "match_type"):
            return "<StoreItemRequirement type={} match_type={} ids={}>".format(
                self.type, self.match_type, self.ids
            )
        if hasattr(self, "balance"):
            return "<StoreItemRequirement type={} balance={}>".format(
                self.type, self.balance
            )
