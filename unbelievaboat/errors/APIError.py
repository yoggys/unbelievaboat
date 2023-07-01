import aiohttp


class APIError(Exception):
    def __init__(self, response: aiohttp.ClientResponse) -> None:
        super().__init__(response)
        self.name: str = self.__class__.__name__
        self.message: str = (
            response.headers.get("data", {}).get("error")
            or response.headers.get("data", {}).get("message")
            or "Unknown error"
        )
        self.status: int = response.status
        self.errors = response.headers.get("data", {}).get("errors")

        self.response: aiohttp.ClientResponse = response
