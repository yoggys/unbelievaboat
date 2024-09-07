from typing import Any, Dict, List, Optional

from ...util.Constants import ItemActionType


class StoreItemAction:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.type: ItemActionType = ItemActionType(data.get("type"))

        if self.type == ItemActionType.RESPOND:
            self.message: str = data.get("message")
        elif self.type in [
            ItemActionType.ADD_ROLES,
            ItemActionType.ADD_ITEMS,
            ItemActionType.REMOVE_ROLES,
            ItemActionType.REMOVE_ITEMS,
        ]:
            self.ids: List[str] = data.get("ids", [])
        elif self.type in [ItemActionType.ADD_BALANCE, ItemActionType.REMOVE_BALANCE]:
            self.balance: Optional[int] = data.get("balance")

    def json(self) -> Dict[str, Any]:
        return {"type": self.type.value, **self.__dict__}

    def __str__(self) -> str:
        if hasattr(self, "message"):
            return "<StoreItemAction type={} message={}>".format(
                self.type, self.message
            )

        if hasattr(self, "ids"):
            return "<StoreItemAction type={} ids={}>".format(self.type, self.ids)

        if hasattr(self, "balance"):
            return "<StoreItemAction type={} balance={}>".format(
                self.type, self.balance
            )
