from typing import Any, Dict, List, Union

import aiohttp

from .RequestHandler import RequestHandler
from .structures import (
    Guild,
    UserInventory,
    InventoryItem,
    Leaderboard,
    Permission,
    Store,
    StoreItem,
    UserBalance,
)
from .util import to_snake_case_deep


class Client:
    def __init__(self, token: str, options: Dict[str, Any] = {}) -> None:
        if not isinstance(token, str):
            raise TypeError("The API token must be a string")
        if not isinstance(options, dict):
            raise TypeError("Options must be a dictionary")

        self.token: str = token
        self.base_url: str = options.get("baseURL", "https://unbelievaboat.com/api")
        self.version: str = f"v{options.get('version', 1)}"

        self._max_retries: int = options.get("maxRetries", 3)
        self._session: aiohttp.ClientSession = aiohttp.ClientSession()

        # Create an instance of the RequestHandler
        self._request_handler: RequestHandler = RequestHandler(self)

    def __str__(self) -> str:
        return "<Client token={}>".format(self.token)

    async def close(self) -> None:
        await self._session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Dict[str, Any] = None,
        data: Dict[str, Any] = None,
    ) -> Any:
        url: str = f"{self.base_url}/{self.version}/{endpoint}"
        headers: Dict[str, str] = {"Authorization": self.token}

        async with self._session.request(
            method, url, headers=headers, params=params, json=data
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def get_user_balance(self, guild_id: int, user_id: int) -> UserBalance:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}"
        response: Dict[str, Any] = await self._request_handler.request("GET", endpoint)
        response["guild_id"] = guild_id
        return UserBalance(self, response)

    async def set_user_balance(
        self, guild_id: int, user_id: int, data: Dict[str, Any] = {}, reason: str = None
    ) -> UserBalance:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}"
        payload: Dict[str, Any] = {
            "cash": data.get("cash"),
            "bank": data.get("bank"),
            "reason": reason,
        }
        response: Dict[str, Any] = await self._request_handler.request(
            "PUT", endpoint, data=payload
        )
        response["guild_id"] = guild_id
        return UserBalance(self, response)

    async def update_user_balance(
        self, guild_id: int, user_id: int, data: Dict[str, Any] = {}, reason: str = None
    ) -> UserBalance:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}"
        payload: Dict[str, Any] = {
            "cash": data.get("cash"),
            "bank": data.get("bank"),
            "reason": reason,
        }
        response: Dict[str, Any] = await self._request_handler.request(
            "PATCH", endpoint, data=payload
        )
        response["guild_id"] = guild_id
        return UserBalance(self, response)

    async def get_guild_leaderboard(
        self, guild_id: int, params: Dict[str, Any] = {}
    ) -> Leaderboard:
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

    async def get_guild_leaderboard_all(
        self, guild_id: int, params: Dict[str, Any] = {}
    ) -> Leaderboard:
        params["limit"] = 2147483647
        return await self.get_guild_leaderboard(guild_id, params)

    async def get_guild(self, guild_id: int) -> Guild:
        endpoint: str = f"guilds/{guild_id}"
        response: Dict[str, Any] = await self._request_handler.request("GET", endpoint)
        return Guild(response)

    async def get_application_permission(self, guild_id: int) -> Permission:
        endpoint: str = f"applications/@me/guilds/{guild_id}"
        response: Dict[str, Any] = await self._request_handler.request("GET", endpoint)
        return Permission(response["permissions"])

    async def get_store_items(
        self, guild_id: int, params: Dict[str, Any] = None
    ) -> Store:
        endpoint: str = f"guilds/{guild_id}/items"
        response: Dict[str, Any] = await self._request_handler.request(
            "GET", endpoint, params=params
        )
        response["guild_id"] = guild_id
        return Store(self, response)

    async def get_store_items_all(
        self, guild_id: int, params: Dict[str, Any] = {}
    ) -> Store:
        params["limit"] = 2147483647
        return await self.get_store_items(guild_id, params)

    async def get_store_item(self, guild_id: int, item_id: int) -> StoreItem:
        endpoint: str = f"guilds/{guild_id}/items/{item_id}"
        response: Dict[str, Any] = await self._request_handler.request("GET", endpoint)
        response["guild_id"] = guild_id
        return StoreItem(self, response)

    async def edit_store_item(
        self,
        guild_id: int,
        item_id: int,
        data: Dict[str, Any],
        params: Dict[str, Any] = None,
    ) -> StoreItem:
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
        self, guild_id: int, user_id: int, params: Dict[str, Any] = None
    ) -> UserInventory:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}/inventory"
        response: Dict[str, Any] = await self._request_handler.request(
            "GET", endpoint, params=params
        )
        response["guild_id"] = guild_id
        response["user_id"] = user_id
        return UserInventory(self, response)

    async def get_inventory_items_all(
        self, guild_id: int, user_id: int, params: Dict[str, Any] = {}
    ) -> UserInventory:
        params["limit"] = 2147483647
        return await self.get_inventory_items(guild_id, user_id, params)

    async def get_inventory_item(
        self, guild_id: int, user_id: int, item_id: int
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
        data: Dict[str, Any],
    ) -> InventoryItem:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}/inventory"
        payload: Dict[str, Any] = {
            "item_id": data.get("item_id"),
            "quantity": data.get("quantity"),
        }
        response: Dict[str, Any] = await self._request_handler.request(
            "POST", endpoint, data=payload
        )
        response["guild_id"] = guild_id
        response["user_id"] = user_id
        return InventoryItem(self, response)

    async def delete_inventory_item(
        self,
        guild_id: int,
        user_id: int,
        item_id: int,
        quantity: int = 1,
    ) -> None:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}/inventory/{item_id}"
        params: Dict[str, Any] = {"quantity": quantity}
        await self._request_handler.request("DELETE", endpoint, params=params)
