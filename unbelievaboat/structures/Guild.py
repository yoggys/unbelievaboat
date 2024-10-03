from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Literal, Optional, Union

from ..utils import MISSING
from .items import InventoryItem, StoreItem
from .Leaderboard import Leaderboard
from .Permission import Permission
from .UserBalance import UserBalance
from .UserInventory import UserInventory

if TYPE_CHECKING:
    from ..Client import Client


class Guild:
    def __init__(self, client: "Client", data: Dict[str, Any]) -> None:
        self.id: int = int(data.get("id"))
        self.name: str = data.get("name")
        self.icon: Optional[str] = data.get("icon")
        self.owner_id: int = int(data.get("owner_id"))
        self.member_count: int = data.get("member_count")
        self.currency_symbol: str = data.get("symbol")

        self._client: "Client" = client
        self._raw_data: Dict[str, Any] = data

    def __str__(self) -> str:
        return "<Guild id={} name='{}' owner_id={} member_count={}>".format(
            self.owner_id, self.name, self.owner_id, self.member_count
        )

    @property
    def icon_url(self) -> Optional[str]:
        if self.icon:
            extension = "gif" if self.icon.startswith("a_") else "png"
            return f"https://cdn.discordapp.com/icons/{self.id}/{self.icon}.{extension}"
        return None

    async def get_application_permission(self) -> Permission:
        return await self._client.get_application_permission(self.id)

    async def get_leaderboard(
        self,
        sort: Literal["cash", "bank", "total"] = "total",
        limit: int = 1000,
        page: int = 1,
        offset: int = 0,
    ) -> Leaderboard:
        return await self._client.get_guild_leaderboard(
            self.id, sort, limit, page, offset
        )

    async def get_full_leaderboard(
        self,
        sort: Literal["cash", "bank", "total"] = "total",
    ) -> Leaderboard:
        return await self._client.get_full_guild_leaderboard(self.id, sort)

    async def get_user_balance(self, user_id: int) -> UserBalance:
        return await self._client.get_user_balance(self.id, user_id)

    async def set_user_balance(
        self,
        user_id: int,
        cash: int = MISSING,
        bank: int = MISSING,
        reason: str = None,
    ) -> UserBalance:
        return await self._client.set_user_balance(
            self.id, user_id, cash=cash, bank=bank, reason=reason
        )

    async def update_user_balance(
        self,
        user_id: int,
        cash: int = MISSING,
        bank: int = MISSING,
        reason: str = None,
    ) -> UserBalance:
        return await self._client.update_user_balance(
            self.id, user_id, cash=cash, bank=bank, reason=reason
        )

    async def add_inventory_item(
        self,
        user_id: int,
        item: Union[int, Union[InventoryItem, StoreItem]],
        quantity: int = 1,
    ) -> InventoryItem:
        item_id = item if isinstance(item, int) else item.id
        return await self._client.add_inventory_item(
            self.id, user_id, item_id, quantity
        )

    async def get_inventory_items(
        self,
        user_id: int,
        sort: Literal["item_id", "name", "quantity"] = "item_id",
        limit: int = 100,
        page: int = 1,
        query: str = MISSING,
    ) -> UserInventory:
        return await self._client.get_inventory_items(
            self.id, user_id, sort=sort, limit=limit, page=page, query=query
        )

    async def get_all_inventory_items(
        self,
        user_id: int,
        sort: Literal["item_id", "name", "quantity"] = "item_id",
        query: str = MISSING,
    ) -> UserInventory:
        return await self._client.get_all_inventory_items(
            self.id, user_id, sort=sort, query=query
        )
