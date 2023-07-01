from typing import Any, Dict, List, Union

import aiohttp

from .RequestHandler import RequestHandler
from .structures import Guild, Leaderboard, Permission, Store, StoreItem, User
from .util import to_snake_case_deep


class Client:
    def __init__(self, token: str, options: Dict[str, Any] = {}) -> None:
        if not isinstance(token, str):
            raise TypeError("The API token must be a string")
        if not isinstance(options, dict):
            raise TypeError("options must be a dictionary")

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

    async def get_user_balance(self, guild_id: int, user_id: int) -> User:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}"
        data: Dict[str, Any] = await self._request_handler.request("GET", endpoint)
        return User(data)

    async def set_user_balance(
        self, guild_id: int, user_id: int, data: Dict[str, Any] = {}, reason: str = None
    ) -> User:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}"
        payload: Dict[str, Any] = {
            "cash": data.get("cash"),
            "bank": data.get("bank"),
            "reason": reason,
        }
        data: Dict[str, Any] = await self._request_handler.request(
            "PUT", endpoint, data=payload
        )
        return User(data)

    async def edit_user_balance(
        self, guild_id: int, user_id: int, data: Dict[str, Any] = {}, reason: str = None
    ) -> User:
        endpoint: str = f"guilds/{guild_id}/users/{user_id}"
        payload: Dict[str, Any] = {
            "cash": data.get("cash"),
            "bank": data.get("bank"),
            "reason": reason,
        }
        data: Dict[str, Any] = await self._request_handler.request(
            "PATCH", endpoint, data=payload
        )
        return User(data)

    async def get_guild_leaderboard(
        self, guild_id: int, params: Dict[str, Any] = {}
    ) -> Dict[str, Union[List[User], int]]:
        endpoint: str = f"guilds/{guild_id}/users"
        data: Dict[str, Any] = await self._request_handler.request(
            "GET", endpoint, params=params
        )

        return Leaderboard(
            {
                "guild_id": guild_id,
                "page": params.get("page", 1),
                "total_pages": data.get("total_pages", 1)
                if "total_pages" in data
                else 1,
                "users": data["users"] if "users" in data else data,
            }
        )

    async def get_guild(self, guild_id: int) -> Guild:
        endpoint: str = f"guilds/{guild_id}"
        data: Dict[str, Any] = await self._request_handler.request("GET", endpoint)
        return Guild(data)

    async def get_application_permission(self, guild_id: int) -> Permission:
        endpoint: str = f"applications/@me/guilds/{guild_id}"
        data: Dict[str, Any] = await self._request_handler.request("GET", endpoint)
        return Permission(data["permissions"])

    async def get_items(
        self, guild_id: int, params: Dict[str, Any] = None
    ) -> Dict[str, Union[int, List[StoreItem]]]:
        endpoint: str = f"guilds/{guild_id}/items"
        data: Dict[str, Any] = await self._request_handler.request(
            "GET", endpoint, params=params
        )

        return Store(
            {
                "guild_id": guild_id,
                "page": data["page"],
                "totalPages": data["total_pages"],
                "items": data["items"],
            }
        )

    async def get_item(self, guild_id: int, item_id: int) -> StoreItem:
        endpoint: str = f"guilds/{guild_id}/items/{item_id}"
        data: Dict[str, Any] = await self._request_handler.request("GET", endpoint)
        return StoreItem(data)

    async def edit_item(
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

        return StoreItem(response)
