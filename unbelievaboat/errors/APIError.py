from __future__ import annotations

from typing import Any, Dict

import aiohttp


class APIError(Exception):
    def __init__(self, data: Dict[str, Any], response: aiohttp.ClientResponse) -> None:
        super().__init__(response)
        self.name: str = self.__class__.__name__
        self.status: int = response.status
        self.message: str = data.get("message") or "Unknown error"

        self.errors = response.headers.get("data", {}).get("errors")
        self.response: aiohttp.ClientResponse = response
