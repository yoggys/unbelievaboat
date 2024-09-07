from typing import Any, List

from ..Client import Client
from .items import StoreItem


class Store:
    def __init__(self, client: Client, data: dict[str, Any]) -> None:
        self.guild_id: int = int(data.get("guild_id"))
        self.items: List[StoreItem] = [
            StoreItem(client, {**item, "guild_id": self.guild_id})
            for item in data.get("items", [])
        ]
        self.total_pages: int = data.get("total_pages", 1)
        self.page: int = data.get("page", 1)

        self._client: Client = client

    def __str__(self) -> str:
        return "<Store guild_id={} items={} total_pages={} page={}>".format(
            self.guild_id,
            [str(item) for item in self.items],
            self.total_pages,
            self.page,
        )

    @property
    def id(self) -> int:
        return self.guild_id

    # TODO: add item methods add, delete, edit
