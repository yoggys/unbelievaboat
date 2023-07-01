from typing import List, Self, Dict, Union

from .items import InventoryItem, StoreItem


class UserInventory:
    def __init__(self, client, data: dict = {}) -> None:
        self.user_id: str = data.get("user_id")
        self.guild_id: str = data.get("guild_id")
        self.items: List[InventoryItem] = [
            InventoryItem(
                client, {**item, "guild_id": self.guild_id, "user_id": self.user_id}
            )
            for item in data.get("items", [])
        ]
        self.total_pages: int = data.get("total_pages", 1)
        self.page: int = data.get("page", 1)

        self._client = client

    def __str__(self) -> str:
        return "<UserInventory guild_id={} items={} total_pages={} page={}>".format(
            self.guild_id,
            [str(item) for item in self.items],
            self.total_pages,
            self.page,
        )

    async def add_item(
        self, item: Union[str, Union[InventoryItem, StoreItem]], quantity: int = 1
    ) -> Self:
        item_id = item if isinstance(item, str) else item.id
        data: Dict[str, any] = {"item_id": item_id, "quantity": quantity}
        added_item = await self._client.add_inventory_item(
            self.guild_id, self.user_id, data
        )
        for item in self.items:
            if item.id == added_item.id:
                item = added_item
                return self
        self.items.append(added_item)
        return self

    async def remove_item(
        self, item: Union[str, Union[InventoryItem, StoreItem]], quantity: int = 1
    ) -> Self:
        item_id = item if isinstance(item, str) else item.id
        await self._client.delete_inventory_item(
            self.guild_id, self.user_id, item_id, quantity
        )

        for item in self.items:
            if item.id == item_id:
                if quantity is None or quantity >= item.quantity:
                    self.items.remove(item)
                else:
                    item.quantity -= quantity
                break

        return self
