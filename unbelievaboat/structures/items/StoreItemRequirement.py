from __future__ import annotations

from typing import Dict, List, Optional, Union

from ...utils import ItemRequirementMatchType, ItemRequirementType


class StoreItemRequirement:
    # noinspection PyUnusedLocal,PyShadowingBuiltins
    def __init__(
        self,
        type: Union[ItemRequirementType, str, int],
        match_type: Optional[Union[ItemRequirementMatchType, str, int]] = None,
        ids: Optional[List[int]] = None,
        balance: Optional[int] = None,
        **kwargs,
    ) -> None:
        self.type: ItemRequirementType = (
            ItemRequirementType[type]
            if isinstance(type, str)
            else ItemRequirementType(type) if isinstance(type, int) else type
        )
        if self.type in [ItemRequirementType.ROLE, ItemRequirementType.ITEM]:
            self.match_type: ItemRequirementMatchType = (
                ItemRequirementMatchType[match_type]
                if isinstance(match_type, str)
                else (
                    ItemRequirementMatchType(match_type)
                    if isinstance(match_type, int)
                    else match_type
                )
            )
            self.ids: List[int] = ids
        elif self.type == ItemRequirementType.TOTAL_BALANCE:
            self.balance: Optional[int] = balance

    def json(self) -> Dict[str, Optional[Union[str, int, List[str]]]]:
        json = {
            "type": self.type.name,
        }
        if self.type in [ItemRequirementType.ROLE, ItemRequirementType.ITEM]:
            json["match_type"] = self.match_type.name
            json["ids"] = [str(id) for id in self.ids]
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
