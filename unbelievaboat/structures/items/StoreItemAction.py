from typing import Any, Dict, List, Optional

from ...util.Constants import ItemActionType


class StoreItemAction:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.type: ItemActionType = ItemActionType(data["type"])

        if self.type == ItemActionType.RESPOND:
            self.message: str = data["message"]
        elif self.type in [
            ItemActionType.ADD_ROLES,
            ItemActionType.ADD_ITEMS,
            ItemActionType.REMOVE_ROLES,
            ItemActionType.REMOVE_ITEMS,
        ]:
            self.ids: List[str] = data.get("ids", [])
        elif self.type in [ItemActionType.ADD_BALANCE, ItemActionType.REMOVE_BALANCE]:
            self.balance: Optional[int] = data.get("balance")

    def toJSON(self) -> dict:
        return {"type": self.type.value, **self.__dict__}

    def __str__(self) -> str:
        return "<StoreItemAction type={} message={} ids={} balance={}>".format(
            self.type, self.message, self.ids, self.balance
        )
