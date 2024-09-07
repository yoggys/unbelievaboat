from typing import Any, Dict, Optional

from typing_extensions import Self

from ...Client import Client
from .BaseItem import BaseItem


class InventoryItem(BaseItem):
    def __init__(self, client: Client, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.guild_id: int = int(data.get("guild_id"))
        self.user_id: int = int(data.get("user_id"))
        self.item_id: int = int(data.get("item_id"))
        self.quantity: int = int(data.get("quantity"))

        self._client: Client = client

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
    def id(self) -> int:
        return self.item_id

    def _update(self, data: Self) -> None:
        self.quantity = data.quantity
        super()._update(data)

    async def add(self, quantity: int = 1) -> Self:
        self._update(
            await self._client.add_inventory_item(
                self.guild_id, self.user_id, self.item_id, quantity
            )
        )
        return self

    async def remove(self, quantity: int = 1) -> Optional[Self]:
        if quantity > self.quantity:
            quantity = self.quantity

        await self._client.remove_inventory_item(
            self.guild_id, self.user_id, self.item_id, quantity
        )

        self.quantity -= quantity
        if self.quantity != 0:
            return self

    async def clear(self) -> None:
        await self._client.remove_inventory_item(
            self.guild_id, self.user_id, self.item_id, self.quantity
        )
        self.quantity = 0
