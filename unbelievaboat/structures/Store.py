from typing import List, Optional

from .items import StoreItem


class Store:
    def __init__(self, data: dict = {}) -> None:
        self.guild_id: Optional[str] = data.get("guild_id")
        self.items = [StoreItem(item) for item in data.get("items", [])]
        self.total_pages: Optional[int] = data.get("total_pages", 1)
        self.page: Optional[int] = data.get("page", 1)

    def __str__(self) -> str:
        return "<Store guild_id={} items={} total_pages={} page={}>".format(
            self.guild_id,
            [str(item) for item in self.items],
            self.total_pages,
            self.page,
        )
