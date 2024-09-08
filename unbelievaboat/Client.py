import asyncio
import atexit
import signal
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

import aiohttp
from typing_extensions import Self

from .RequestHandler import RequestHandler
from .structures import (
    Guild,
    InventoryItem,
    Leaderboard,
    Permission,
    Store,
    StoreItem,
    StoreItemAction,
    StoreItemRequirement,
    UserBalance,
    UserInventory,
)
from .utils import MISSING


class Client:
    def __init__(
        self,
        token: str,
        version: Optional[int] = 1,
        max_retries: Optional[int] = 3,
        base_url: Optional[str] = "https://unbelievaboat.com/api",
    ) -> None:
        if not isinstance(token, str):
            raise TypeError("The API token must be a string")

        self._token: str = token
        self._base_url: str = base_url
        self._version: str = f"v{version}"

        self._max_retries: int = max_retries
        self._session: aiohttp.ClientSession = aiohttp.ClientSession()

        self._request_handler: RequestHandler = RequestHandler(self)

        atexit.register(self._close_sync)
        signal.signal(signal.SIGINT, self._handle_exit)
        signal.signal(signal.SIGTERM, self._handle_exit)

    def __str__(self) -> str:
        return "<Client base_url={}, version={}, max_retries={}>".format(
            self._base_url, self._version, self._max_retries
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def close(self) -> None:
        if not self._session.closed:
            await self._session.close()

    def _close_sync(self) -> None:
        if not self._session.closed:
            asyncio.run(self.close())

    def _handle_exit(self, signum, frame) -> None:
        if not self._session.closed:
            asyncio.run(self.close())

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Dict[str, Any] = None,
        data: Dict[str, Any] = None,
    ) -> Any:
        url: str = f"{self._base_url}/{self._version}/{endpoint}"
        headers: Dict[str, str] = {"Authorization": self._token}

        async with self._session.request(
            method, url, headers=headers, params=params, json=data
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def get_application_permission(self, guild_id: int) -> Permission:
        endpoint: str = f"applications/@me/guilds/{guild_id}"
        response: Dict[str, Any] = await self._request_handler.request("GET", endpoint)
        return Permission(guild_id, response.get("permissions"))

    async def get_guild(self, guild_id: int) -> Guild:
        endpoint: str = f"guilds/{guild_id}"
        response: Dict[str, Any] = await self._request_handler.request("GET", endpoint)
        return Guild(self, response)

    async def get_guild_leaderboard(
        self,
        guild_id: int,
        sort: Optional[Literal["cash", "bank", "total"]] = "total",
        limit: Optional[int] = 1000,
        page: Optional[int] = 1,
        offset: Optional[int] = 0,
    ) -> Leaderboard:
        if offset != 0 and page != 1:
            raise ValueError("Offset and page are mutually exclusive")

        params = {
            "sort": sort,
            "limit": limit,
            "page": page,
            "offset": offset,
        }

        endpoint: str = f"guilds/{guild_id}/users"
        response: Dict[str, Any] = await self._request_handler.request(
            "GET", endpoint, params=params
        )

        data: Dict[str, Any] = {
            "guild_id": guild_id,
        }

        if isinstance(response, list):
            data["users"] = response
        else:
            data.update(
                **{
                    "users": response.get("users", []),
                    "page": params.get("page", 1),
                    "total_pages": response.get("total_pages", 1),
                }
            )
        return Leaderboard(self, data)

    async def get_full_guild_leaderboard(
        self,
        guild_id: int,
        sort: Optional[Literal["cash", "bank", "total"]] = "total",
    ) -> Leaderboard:
        return await self.get_guild_leaderboard(guild_id, sort=sort, limit=2147483647)

    async def get_store_items(
        self,
        guild_id: int,
        sort: Optional[
            Literal["id", "price", "name", "stock_remaining", "expires_at"]
        ] = "id",
        limit: Optional[int] = 100,
        page: Optional[int] = 1,
        query: Optional[str] = None,
    ) -> Store:
        params = {
            "sort": sort,
            "limit": limit,
            "page": page,
            "query": query,
        }

        endpoint: str = f"guilds/{guild_id}/items"
        response: Dict[str, Any] = await self._request_handler.request(
            "GET", endpoint, params=params
        )
        response["guild_id"] = guild_id
        return Store(self, response)

    async def get_all_store_items(
        self,
        guild_id: int,
        sort: Optional[
            Literal["id", "price", "name", "stock_remaining", "expires_at"]
        ] = "id",
        query: Optional[str] = None,
    ) -> Store:
        return await self.get_store_items(
            guild_id, sort=sort, query=query, limit=2147483647
        )

    async def get_store_item(self, guild_id: int, item_id: int) -> StoreItem:
        endpoint: str = f"guilds/{guild_id}/items/{item_id}"
        response: Dict[str, Any] = await self._request_handler.request("GET", endpoint)
        response["guild_id"] = guild_id
        return StoreItem(self, response)

    async def edit_store_item(
        self,
        guild_id: int,
        item_id: int,
        name: Optional[str] = MISSING,
        price: Optional[int] = MISSING,
        description: Optional[str] = MISSING,
        is_inventory: Optional[bool] = MISSING,
        is_usable: Optional[bool] = MISSING,
        is_sellable: Optional[bool] = MISSING,
        stock_remaining: Optional[int] = MISSING,
        unlimited_stock: Optional[bool] = MISSING,
        requirements: Optional[List[StoreItemRequirement]] = MISSING,
        actions: Optional[List[StoreItemAction]] = MISSING,
        expires_at: Optional[datetime] = MISSING,
        emoji_unicode: Optional[str] = MISSING,
        emoji_id: Optional[int] = MISSING,
        cascade_update: Optional[bool] = MISSING,
    ) -> StoreItem:
        data = {}
        if name is not MISSING:
            data["name"] = name
        if price is not MISSING:
            data["price"] = price
        if description is not MISSING:
            data["description"] = description
        if is_inventory is not MISSING:
            data["is_inventory"] = is_inventory
        if is_usable is not MISSING:
            data["is_usable"] = is_usable
        if is_sellable is not MISSING:
            data["is_sellable"] = is_sellable
        if stock_remaining is not MISSING:
            data["stock_remaining"] = stock_remaining
        if unlimited_stock is not MISSING:
            data["unlimited_stock"] = unlimited_stock
        if requirements is not MISSING:
            data["requirements"] = (
                [requirement.json() for requirement in requirements]
                if requirements
                else None
            )
        if actions is not MISSING:
            data["actions"] = [action.json() for action in actions] if actions else None
        if expires_at is not MISSING:
            data["expires_at"] = expires_at.isoformat() if expires_at else None
        if emoji_unicode is not MISSING:
            data["emoji_unicode"] = emoji_unicode
        if emoji_id is not MISSING:
            data["emoji_id"] = emoji_id

        params = {
            "cascade_update": cascade_update,
        }

        endpoint: str = f"guilds/{guild_id}/items/{item_id}"
        response: Dict[str, Any] = await self._request_handler.request(
            "PATCH", endpoint, data=data, params=params
        )
        response["guild_id"] = guild_id
        return StoreItem(self, response)

    async def delete_store_item(
        self,
        guild_id: int,
        item_id: int,
        cascade: bool = False,
    ) -> None:
        endpoint: str = f"guilds/{guild_id}/items/{item_id}"
        params: Dict[str, Any] = {"cascade": cascade}
        await self._request_handler.request("DELETE", endpoint, params=params)

    async def get_inventory_items(
        self,
        guild_id: int,
        user_id: int,
        sort: Optional[Literal["item_id", "name", "quantity"]] = "item_id",
        limit: Optional[int] = 100,
        page: Optional[int] = 1,
        query: Optional[str] = None,
    ) -> UserInventory:
        params = {"sort": sort, "limit": limit, "page": page, "query": query}

        endpoint: str = f"guilds/{guild_id}/users/{user_id}/inventory"
        response: Dict[str, Any] = await self._request_handler.request(
            "GET", endpoint, params=params
        )
        response["guild_id"] = guild_id
        response["user_id"] = user_id
        return UserInventory(self, response)

    async def get_all_inventory_items(
        self,
        guild_id: int,
        user_id: int,
        sort: Optional[Literal["item_id", "name", "quantity"]] = "item_id",
        query: Optional[str] = None,
    ) -> UserInventory:
        return await self.get_inventory_items(
            guild_id, user_id, sort=sort, query=query, limit=2147483647
        )

    async def get_inventory_item(
        self,
        guild_id: int,
        user_id: int,
        item_id: int,
    ) -> InventoryItem:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}/inventory/{item_id}"
        response: Dict[str, Any] = await self._request_handler.request("GET", endpoint)
        response["guild_id"] = guild_id
        response["user_id"] = user_id
        return InventoryItem(self, response)

    async def add_inventory_item(
        self,
        guild_id: int,
        user_id: int,
        item_id: int,
        quantity: int = 1,
    ) -> InventoryItem:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}/inventory"
        payload: Dict[str, Any] = {
            "item_id": item_id,
            "quantity": quantity,
        }
        response: Dict[str, Any] = await self._request_handler.request(
            "POST", endpoint, data=payload
        )
        response["guild_id"] = guild_id
        response["user_id"] = user_id
        return InventoryItem(self, response)

    async def remove_inventory_item(
        self,
        guild_id: int,
        user_id: int,
        item_id: int,
        quantity: int = 1,
    ) -> None:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}/inventory/{item_id}"
        params: Dict[str, Any] = {"quantity": quantity}
        await self._request_handler.request("DELETE", endpoint, params=params)

    async def get_user_balance(self, guild_id: int, user_id: int) -> UserBalance:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}"
        response: Dict[str, Any] = await self._request_handler.request("GET", endpoint)
        response["guild_id"] = guild_id
        return UserBalance(self, response)

    async def set_user_balance(
        self,
        guild_id: int,
        user_id: int,
        cash: Optional[int] = None,
        bank: Optional[int] = None,
        reason: str = None,
    ) -> UserBalance:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}"
        payload: Dict[str, Any] = {
            "cash": cash,
            "bank": bank,
            "reason": reason,
        }
        response: Dict[str, Any] = await self._request_handler.request(
            "PUT", endpoint, data=payload
        )
        response["guild_id"] = guild_id
        return UserBalance(self, response)

    async def update_user_balance(
        self,
        guild_id: int,
        user_id: int,
        cash: Optional[int] = None,
        bank: Optional[int] = None,
        reason: str = None,
    ) -> UserBalance:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}"
        payload: Dict[str, Any] = {
            "cash": cash,
            "bank": bank,
            "reason": reason,
        }
        response: Dict[str, Any] = await self._request_handler.request(
            "PATCH", endpoint, data=payload
        )
        response["guild_id"] = guild_id
        return UserBalance(self, response)
