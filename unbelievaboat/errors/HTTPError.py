import aiohttp


class HTTPError(Exception):
    def __init__(self, response: aiohttp.ClientResponse) -> None:
        super().__init__(response)
        self.name: str = self.__class__.__name__
        self.status: int = response.status
        self.message: str = (
            response.status_text
            if hasattr(response, "status_text")
            else "Unknown error"
        )

        self.response: aiohttp.ClientResponse = response

    def __str__(self):
        return f"HTTP Error {self.status}: {self.message}"
