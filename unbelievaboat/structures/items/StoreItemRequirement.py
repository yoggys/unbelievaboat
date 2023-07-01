from typing import Any, Dict, List, Optional

from ...util.Constants import ItemRequirementMatchType, ItemRequirementType


class StoreItemRequirement:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.type: ItemRequirementType = ItemRequirementType(data["type"])

        if self.type in [ItemRequirementType.ROLE, ItemRequirementType.ITEM]:
            self.matchType: ItemRequirementMatchType = ItemRequirementMatchType(
                data["match_type"]
            )
            self.ids: List[str] = data.get("ids", [])
        elif self.type == ItemRequirementType.TOTAL_BALANCE:
            self.balance: Optional[int] = data.get("balance")

    def toJSON(self) -> dict:
        json = {
            "type": self.type.value,
            "matchType": self.matchType.value if self.matchType else None,
        }
        if self.type in [ItemRequirementType.ROLE, ItemRequirementType.ITEM]:
            json["ids"] = self.ids
        elif self.type == ItemRequirementType.TOTAL_BALANCE:
            json["balance"] = self.balance
        return json

    def __str__(self) -> str:
        return "<StoreItemRequirement type={} matchType={} ids={} balance={}>".format(
            self.type, self.matchType, self.ids, self.balance
        )
