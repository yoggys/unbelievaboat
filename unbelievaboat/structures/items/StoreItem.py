from datetime import datetime
from typing import Any, Dict, List, Optional

from typing_extensions import Self

from ...Client import Client
from . import BaseItem, StoreItemAction, StoreItemRequirement


class StoreItem(BaseItem):
    def __init__(self, client: Client, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.guild_id: int = int(data.get("guild_id"))
        self.id: int = int(data.get("id"))
        self.price: int = int(data.get("price"))
        self.is_inventory: bool = data.get("is_inventory")
        self.stock_remaining: int = data.get("stock_remaining")
        self.unlimited_stock: bool = data.get("unlimited_stock")
        self.expires_at: datetime = (
            datetime.strptime(data.get("expires_at"), "%Y-%m-%dT%H:%M:%S.%fZ")
            if data.get("expires_at")
            else None
        )

        self._client: Client = client

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

    def _update(self, data: Self) -> None:
        self.price = data.price
        self.is_inventory = data.is_inventory
        self.stock_remaining = data.stock_remaining
        self.unlimited_stock = data.unlimited_stock
        self.expires_at = data.expires_at
        super()._update(data)

    async def edit(
        self,
        name: Optional[str] = None,
        price: Optional[int] = None,
        description: Optional[str] = None,
        is_inventory: Optional[bool] = None,
        is_usable: Optional[bool] = None,
        is_sellable: Optional[bool] = None,
        stock_remaining: Optional[int] = None,
        unlimited_stock: Optional[bool] = None,
        requirements: Optional[List[StoreItemRequirement]] = None,
        actions: Optional[List[StoreItemAction]] = None,
        expires_at: Optional[datetime] = None,
        emoji_unicode: Optional[str] = None,
        emoji_id: Optional[int] = None,
        cascade_update: Optional[bool] = False,
    ) -> Self:
        # TODO: replace default values with MISSING
        self._update(
            await self._client.edit_store_item(
                self.guild_id,
                self.id,
                name,
                price,
                description,
                is_inventory,
                is_usable,
                is_sellable,
                stock_remaining,
                unlimited_stock,
                requirements,
                actions,
                expires_at,
                emoji_unicode,
                emoji_id,
                cascade_update,
            )
        )
        return self

    async def delete(self, cascade: bool = False) -> None:
        await self._client.delete_store_item(self.guild_id, self.id, cascade)
