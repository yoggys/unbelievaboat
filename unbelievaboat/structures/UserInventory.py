import asyncio
from typing import Any, Dict, List, Optional, Union

from typing_extensions import Self

from ..Client import Client
from .items import InventoryItem, StoreItem


class UserInventory:
    def __init__(self, client: Client, data: Dict[str, Any]) -> None:
        self.guild_id: int = int(data.get("guild_id"))
        self.user_id: int = int(data.get("user_id"))
        self.items: List[InventoryItem] = [
            InventoryItem(
                client, {**item, "guild_id": self.guild_id, "user_id": self.user_id}
            )
            for item in data.get("items", [])
        ]
        self.total_pages: int = data.get("total_pages", 1)
        self.page: int = data.get("page", 1)

        self._client: Client = client

    def __str__(self) -> str:
        return "<UserInventory guild_id={} items={} total_pages={} page={}>".format(
            self.guild_id,
            [str(item) for item in self.items],
            self.total_pages,
            self.page,
        )

    @property
    def id(self) -> int:
        return self.user_id

    async def add(
        self, item: Union[int, Union[InventoryItem, StoreItem]], quantity: int = 1
    ) -> Self:
        item_id = item if isinstance(item, int) else item.id
        added_item = await self._client.add_inventory_item(
            self.guild_id, self.user_id, item_id, quantity
        )
        for index, item in enumerate(self.items):
            if item.id == added_item.id:
                self.items[index] = added_item
                return self
        self.items.append(added_item)
        return self

    async def remove(
        self, item: Union[int, Union[InventoryItem, StoreItem]], quantity: int = 1
    ) -> Self:
        item_id = item if isinstance(item, int) else item.id
        await self._client.remove_inventory_item(
            self.guild_id, self.user_id, item_id, quantity
        )

        for index, item in enumerate(self.items):
            if item.id == item_id:
                if quantity >= item.quantity:
                    self.items.remove(item)
                else:
                    self.items[index].quantity -= quantity
                break
        return self

    async def clear(
        self, item: Optional[Union[int, Union[InventoryItem, StoreItem]]] = None
    ) -> Self:
        if not item:
            await asyncio.gather(
                *[self.remove(item, item.quantity) for item in self.items]
            )
            self.items.clear()
            return self

        item_id = item if isinstance(item, int) else item.id
        for item in self.items:
            if item.id == item_id:
                await self.remove(item, item.quantity)
                self.items.remove(item)
                break
        return self
