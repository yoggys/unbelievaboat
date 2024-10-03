from __future__ import annotations

import asyncio
from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Union

from typing_extensions import Self

from ..utils import MISSING
from .items import InventoryItem, StoreItem, StoreItemAction, StoreItemRequirement

if TYPE_CHECKING:
    from ..Client import Client


class Store:
    def __init__(self, client: "Client", data: dict[str, Any]) -> None:
        self.guild_id: int = int(data.get("guild_id"))
        self.items: List[StoreItem] = [
            StoreItem(client, {**item, "guild_id": self.guild_id})
            for item in data.get("items", [])
        ]
        self.total_pages: int = data.get("total_pages", 1)
        self.page: int = data.get("page", 1)

        self._client: "Client" = client

    def __str__(self) -> str:
        return "<Store guild_id={} items={} total_pages={} page={}>".format(
            self.guild_id,
            [str(item) for item in self.items],
            self.total_pages,
            self.page,
        )

    @property
    def id(self) -> int:
        return self.guild_id

    async def remove(
        self, item: Union[int, StoreItem, InventoryItem], cascade: bool = False
    ) -> Self:
        item_id = item if isinstance(item, int) else item.id
        await self._client.delete_store_item(self.guild_id, item_id, cascade)

        for item in self.items:
            if item.id == item_id:
                self.items.remove(item)
                break
        return self

    async def clear(self, cascade: bool = False) -> Self:
        await asyncio.gather(*[self.remove(item, cascade) for item in self.items])
        self.items.clear()
        return self

    async def create(
        self,
        name: str = MISSING,
        price: int = MISSING,
        description: str = MISSING,
        is_inventory: bool = MISSING,
        is_usable: bool = MISSING,
        is_sellable: bool = MISSING,
        stock_remaining: int = MISSING,
        unlimited_stock: bool = MISSING,
        requirements: List[StoreItemRequirement] = MISSING,
        actions: List[StoreItemAction] = MISSING,
        expires_at: datetime = MISSING,
        emoji_unicode: str = MISSING,
        emoji_id: int = MISSING,
    ) -> Self:
        self.items.append(
            await self._client.create_store_item(
                self.guild_id,
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
            )
        )
        return self

    async def edit(
        self,
        item: Union[int, StoreItem, InventoryItem],
        name: str = MISSING,
        price: int = MISSING,
        description: str = MISSING,
        is_inventory: bool = MISSING,
        is_usable: bool = MISSING,
        is_sellable: bool = MISSING,
        stock_remaining: int = MISSING,
        unlimited_stock: bool = MISSING,
        requirements: List[StoreItemRequirement] = MISSING,
        actions: List[StoreItemAction] = MISSING,
        expires_at: datetime = MISSING,
        emoji_unicode: str = MISSING,
        emoji_id: int = MISSING,
        cascade_update: bool = False,
    ) -> Self:
        item_id = item if isinstance(item, int) else item.id
        data = await self._client.edit_store_item(
            self.guild_id,
            item_id,
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

        for index, item in enumerate(self.items):
            if item.id == item_id:
                self.items[index] = data
                break

        return self
