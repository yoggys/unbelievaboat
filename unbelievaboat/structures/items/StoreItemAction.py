from typing import Any, Dict, List, Optional

from ...utils.Constants import ItemActionType


class StoreItemAction:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.type: ItemActionType = ItemActionType[data.get("type")]

        if self.type == ItemActionType.RESPOND:
            # TODO: message object is {content: string, embeds: array}
            self.message: str = data.get("message")
        elif self.type in [
            ItemActionType.ADD_ROLES,
            ItemActionType.ADD_ITEMS,
            ItemActionType.REMOVE_ROLES,
            ItemActionType.REMOVE_ITEMS,
        ]:
            self.ids: List[int] = data.get("ids", [])
        elif self.type in [ItemActionType.ADD_BALANCE, ItemActionType.REMOVE_BALANCE]:
            self.balance: Optional[int] = data.get("balance")

    def json(self) -> Dict[str, Any]:
        json = {"type": self.type.name}
        if hasattr(self, "message"):
            json["message"] = self.message
        elif hasattr(self, "ids"):
            json["ids"] = self.ids
        elif hasattr(self, "balance"):
            json["balance"] = self.balance
        return json

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
