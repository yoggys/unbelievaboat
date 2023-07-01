from typing import Any, Dict, List

from .UserBalance import UserBalance


class Leaderboard:
    def __init__(self, client, data: Dict[str, Any] = {}) -> None:
        self.guild_id: str = data.get("guild_id")
        self.users: List[UserBalance] = [
            UserBalance(client, {**user, "guild_id": self.guild_id})
            for user in data.get("users", [])
        ]
        self.total_pages: int = data.get("total_pages")
        self.page: int = data.get("page")

    def __str__(self) -> str:
        return "<Leaderboard guild_id={} users={} total_pages={} page={}>".format(
            self.guild_id,
            [str(user) for user in self.users],
            self.total_pages,
            self.page,
        )
