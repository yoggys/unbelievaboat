from datetime import datetime
from typing import Any, Dict

from typing_extensions import Self

from .BaseItem import BaseItem


class StoreItem(BaseItem):
    def __init__(self, client, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.guild_id: str = data["guild_id"]
        self.id: str = data["id"]
        self.price: int = int(data["price"])
        self.is_inventory: bool = data["is_inventory"]
        self.stock_remaining: int = data["stock_remaining"]
        self.unlimited_stock: bool = data["unlimited_stock"]
        self.expires_at: datetime = (
            datetime.strptime(data["expires_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            if data.get("expires_at")
            else None
        )

        self._client = client

    def __str__(self) -> str:
        return "<StoreItem id={} guild_id={} price={} is_inventory={} stock_remaining={} unlimited_stock={} expires_at={} actions={} requirements={}>".format(
            self.id,
            self.guild_id,
            self.price,
            self.is_inventory,
            self.stock_remaining,
            self.unlimited_stock,
            self.expires_at,
            [str(a) for a in self.actions],
            [str(r) for r in self.requirements],
        )

    async def edit(
        self, data: Dict[str, Any] = {}, params: Dict[str, Any] = {}
    ) -> Self:
        self = await self._client.edit_store_item(self.guild_id, self.id, data, params)
        return self

    async def delete(self, cascade: bool = False) -> None:
        self = await self._client.delete_item(self.guild_id, self.id, cascade)
