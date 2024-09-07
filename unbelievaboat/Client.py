from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

import aiohttp

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
from .util import to_snake_case_deep


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

        # Create an instance of the RequestHandler
        self._request_handler: RequestHandler = RequestHandler(self)

    def __str__(self) -> str:
        return "<Client _base_url={}, _version={}, max_retries={}>".format(
            self._base_url, self._version, self._max_retries
        )

    async def close(self) -> None:
        await self._session.close()

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
    ) -> StoreItem:
        data = {
            "name": name,
            "price": price,
            "description": description,
            "is_inventory": is_inventory,
            "is_usable": is_usable,
            "is_sellable": is_sellable,
            "stock_remaining": stock_remaining,
            "unlimited_stock": unlimited_stock,
            "requirements": [requirement.json() for requirement in requirements],
            "actions": [action.json() for action in actions],
            "expires_at": expires_at.isoformat(),
            "emoji_unicode": emoji_unicode,
            "emoji_id": emoji_id,
        }
        params = {
            "cascade_update": cascade_update,
        }

        endpoint: str = f"guilds/{guild_id}/items/{item_id}"
        payload: Dict[str, Any] = to_snake_case_deep(data)
        response: Dict[str, Any] = await self._request_handler.request(
            "PATCH", endpoint, data=payload, params=params
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
