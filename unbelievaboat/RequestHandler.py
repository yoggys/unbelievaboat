import asyncio
import time
from typing import Any, Dict, Optional

from .errors import APIError, HTTPError


class RequestHandler:
    def __init__(self, client) -> None:
        self._client = client
        self.locks: Dict[str, asyncio.Lock] = {}

    def __str__(self) -> str:
        return "<RequestHandler>"

    async def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        _attempts: int = 0,
    ) -> Any:
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
    ):
        async with self.locks[route]:
            url = "{}/{}/{}".format(
                self._client.base_url, self._client.version, endpoint
            )
            options = {
                "headers": {
                    "Authorization": self._client.token,
                    "Content-Type": "application/json",
                },
                "url": url,
                "method": method,
                "json": data,
                "params": params,
            }

            async with self._client._session.request(
                **options
            ) as response:  # type: ClientResponse
                _attempts += 1

                # Handle rate limits
                await self.parse_rate_limit_headers(response.headers)

                if response.status >= 200 and response.status < 300:
                    try:
                        return await response.json()
                    except Exception as e:
                        return await response.text()

                if response.status == 429:
                    if _attempts >= self._client._max_retries:
                        raise APIError(await response.json(), response)
                    else:
                        await self.request(method, endpoint, data, params, _attempts)

                raise HTTPError(await response.json(), response)

    def get_route(self, method: str, endpoint: str) -> str:
        import re

        major_params = ["guilds"]
        route = re.sub(
            r"/([a-z-]+)/(?:(\d+))",
            lambda match: match.group()
            if match.group(1) in major_params
            else f"/{match.group(1)}/:id",
            endpoint,
        )
        return f"{method}/{route}"

    async def parse_rate_limit_headers(self, headers: Dict[str, str]) -> None:
        remaining = int(headers.get("x-ratelimit-remaining", 0))
        if remaining <= 0:
            if headers.get("retry-after"):
                retry_after = float(headers.get("retry-after", 0)) / 1000
                await asyncio.sleep(retry_after)
            else:
                reset_after = (
                    float(headers.get("x-ratelimit-reset", 0)) / 1000 - time.time()
                )
                await asyncio.sleep(reset_after)
