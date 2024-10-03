from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from ...utils import ItemActionType
from ..Message import Message


class StoreItemAction:
    # noinspection PyUnusedLocal,PyShadowingBuiltins
    def __init__(
        self,
        type: Union[ItemActionType, str, int],
        message: Optional[Union[Message, Dict[str, Any]]] = None,
        ids: Optional[List[int]] = None,
        balance: Optional[int] = None,
        **kwargs,
    ) -> None:
        self.type: ItemActionType = (
            ItemActionType[type]
            if isinstance(type, str)
            else ItemActionType(type) if isinstance(type, int) else type
        )
        if self.type == ItemActionType.RESPOND:
            self.message: Message = (
                message if isinstance(message, Message) else Message(**message)
            )
        elif self.type in [
            ItemActionType.ADD_ROLES,
            ItemActionType.ADD_ITEMS,
            ItemActionType.REMOVE_ROLES,
            ItemActionType.REMOVE_ITEMS,
        ]:
            self.ids: List[int] = ids
        elif self.type in [ItemActionType.ADD_BALANCE, ItemActionType.REMOVE_BALANCE]:
            self.balance: Optional[int] = balance

    def json(self) -> Dict[str, Any]:
        json = {"type": self.type.name}
        if hasattr(self, "message"):
            json["message"] = self.message.json()
        elif hasattr(self, "ids"):
            json["ids"] = [str(id) for id in self.ids]
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
