import asyncio
import re
import time
from typing import Any, Dict, List, Optional, Union

from aiohttp import ClientResponse

from .Client import Client
from .errors import APIError, HTTPError


class RequestHandler:
    def __init__(self, client: Client) -> None:
        self._client: Client = client
        self.locks: Dict[str, asyncio.Lock] = {}
        self.timeouts: Dict[str, float] = {}

    def __str__(self) -> str:
        return "<RequestHandler>"

    @staticmethod
    def get_route(method: str, endpoint: str) -> str:
        major_params = ["guilds"]
        route = re.sub(
            r"/([a-z-]+)/(?:(\d+))",
            lambda match: (
                match.group()
                if match.group(1) in major_params
                else f"/{match.group(1)}/:id"
            ),
            endpoint,
        )
        return f"{method}/{route}"

    def get_url(self, endpoint: str) -> str:
        return "{}/{}/{}".format(
            self._client._base_url, self._client._version, endpoint
        )

    def get_data(
        self,
        url: str,
        method: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return {
            "headers": {
                "Authorization": self._client._token,
                "Content-Type": "application/json",
            },
            "url": url,
            "method": method,
            "json": data,
            "params": params,
        }

    async def check_ratelimit(self, route: str) -> None:
        if route in self.timeouts:
            timeout = self.timeouts[route] - time.time()
            if timeout > 0:
                await asyncio.sleep(timeout)
            del self.timeouts[route]

    def handle_ratelimit(self, route: str, response: ClientResponse) -> None:
        remaining = int(response.headers.get("x-ratelimit-remaining", 0))
        if remaining <= 0:
            if response.headers.get("retry-after"):
                self.timeouts[route] = (
                    time.time() + float(response.headers.get("retry-after", 0)) / 1000
                )
            else:
                self.timeouts[route] = (
                    float(response.headers.get("x-ratelimit-reset", 0)) / 1000
                )

    async def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        _attempts: int = 0,
    ) -> Union[Dict[str, Any], List[Any], str]:
        route = self.get_route(method, endpoint)
        if route not in self.locks:
            self.locks[route] = asyncio.Lock()

        return await self.execute_request(
            route, method, endpoint, data, params, _attempts
        )

    async def execute_request(
        self,
        route: str,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        _attempts: int = 0,
    ) -> Union[Dict[str, Any], List[Any], str]:
        async with self.locks[route]:
            await self.check_ratelimit(route)

            url = self.get_url(endpoint)
            options = self.get_data(url, method, data, params)

            async with self._client._session.request(
                **options
            ) as response:  # type: ClientResponse
                _attempts += 1

                self.handle_ratelimit(route, response)

                if 200 <= response.status < 300:
                    if response.content_type == "application/json":
                        return await response.json()
                    else:
                        return await response.text()

                if response.status == 429:
                    if _attempts >= self._client._max_retries:
                        raise APIError(await response.json(), response)
                    else:
                        await self.request(method, endpoint, data, params, _attempts)

                raise HTTPError(await response.json(), response)
