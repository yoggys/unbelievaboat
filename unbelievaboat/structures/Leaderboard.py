from typing import Any, Dict, List, Optional

from .UserBalance import UserBalance


class Leaderboard:
    def __init__(self, client, data: Dict[str, Any] = {}) -> None:
        self.guild_id: str = data.get("guild_id")
        self.users: List[UserBalance] = [
            UserBalance(client, {**user, "guild_id": self.guild_id})
            for user in data.get("users", [])
        ]
        self.total_pages: Optional[int] = data.get("total_pages")
        self.page: Optional[int] = data.get("page")

    def __str__(self) -> str:
        if self.total_pages:
            return "<Leaderboard guild_id={} users={} total_pages={} page={}>".format(
                self.guild_id,
                [str(user) for user in self.users],
                self.total_pages,
                self.page,
            )
        return "<Leaderboard guild_id={} users={}>".format(
            self.guild_id, [str(user) for user in self.users]
        )
