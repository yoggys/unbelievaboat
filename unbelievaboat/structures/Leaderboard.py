from typing import Any, Dict, List

from .User import User


class Leaderboard:
    def __init__(self, client, data: Dict[str, Any] = {}) -> None:
        self.guild_id: str = data.get("guild_id")
        self.users: List[User] = [
            User(client, {**user, "guild_id": self.guild_id})
            for user in data.get("users", [])
        ]
        self.total_pages: int = data.get("total_pages", 1)
        self.page: int = data.get("page", 1)

    def __str__(self) -> str:
        return "<Leaderboard guild_id={} users={} total_pages={} page={}>".format(
            self.guild_id,
            [str(user) for user in self.users],
            self.total_pages,
            self.page,
        )
