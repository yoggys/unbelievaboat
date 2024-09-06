from typing import Any, Dict, Optional
from typing_extensions import Self

from .BaseItem import BaseItem


class InventoryItem(BaseItem):
    def __init__(self, client, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.guild_id: str = data["guild_id"]
        self.user_id: str = data["user_id"]
        self.item_id: str = data["item_id"]
        self.quantity: int = int(data["quantity"])

        self._client = client

    def __str__(self) -> str:
        return "<InventoryItem item_id={} guild_id={} user_id={} quantity={} actions={} requirements={}>".format(
            self.item_id,
            self.guild_id,
            self.user_id,
            self.quantity,
            [str(a) for a in self.actions],
            [str(r) for r in self.requirements],
        )

    @property
    def id(self) -> str:
        return self.item_id

    async def delete(self, quantity: int = 1) -> Optional[Self]:
        await self._client.delete_inventory_item(
            self.guild_id, self.user_id, self.item_id, quantity
        )
        if quantity is None or quantity >= self.quantity:
            return None
        return self
