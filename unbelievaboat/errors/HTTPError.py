from typing import Any, Dict

import aiohttp


class HTTPError(Exception):
    def __init__(self, status: int, data: Dict[str, Any], response: aiohttp.ClientResponse) -> None:
        super().__init__(response)
        self.name: str = self.__class__.__name__
        self.status: int = status
        self.message: str = data.get("message") or "Unknown error"

        self.response: aiohttp.ClientResponse = response

    def __str__(self):
        return f"HTTP Error {self.status}: {self.message}"
