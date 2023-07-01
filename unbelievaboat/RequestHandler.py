import json
from typing import Any, Dict, Optional

from .errors import APIError, HTTPError
from .util import Bucket


class RequestHandler:
    def __init__(self, client) -> None:
        self._client = client
        self.ratelimits: Dict[str, Bucket] = {}

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
        if route not in self.ratelimits:
            self.ratelimits[route] = Bucket()

        async with self.ratelimits[route].semaphore:
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
                # Increase the number of attempts
                _attempts += 1

                # Add the rate limit header data to the bucket
                self.parse_rate_limit_headers(route, response.headers)

                if response.status >= 200 and response.status < 300:
                    try:
                        return await response.json()
                    except:
                        return json.dumps(await response.text())

                if response.status == 429:
                    if _attempts >= self._client._max_retries:
                        raise APIError(response)
                    else:
                        await self.request(method, endpoint, data, params, _attempts)

                raise HTTPError(response.status, await response.json())

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

    def parse_rate_limit_headers(self, route: str, headers: Dict[str, str]) -> None:
        import time

        now = time.time()

        self.ratelimits[route].limit = int(headers.get("x-ratelimit-limit", 0))

        remaining = headers.get("x-ratelimit-remaining")
        self.ratelimits[route].remaining = (
            int(remaining) if remaining is not None else 1
        )

        retry_after = headers.get("retry-after")
        if retry_after:
            self.ratelimits[route].reset = int(retry_after) + now
        else:
            reset_time = headers.get("x-ratelimit-reset")
            self.ratelimits[route].reset = (
                max(int(reset_time), now) if reset_time else now
            )
