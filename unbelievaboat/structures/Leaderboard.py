from typing import List, Optional

from .User import User


class Leaderboard:
    def __init__(self, data: dict = {}) -> None:
        self.guild_id: Optional[str] = data.get("guild_id")
        self.users: Optional[List[User]] = [
            User(user) for user in data.get("users", [])
        ]
        self.total_pages: Optional[int] = data.get("total_pages")
        self.page: Optional[int] = data.get("page", 1)

    def __str__(self) -> str:
        return "<Leaderboard guild_id={} users={} total_pages={} page={}>".format(
            self.guild_id,
            [str(user) for user in self.users],
            self.total_pages,
            self.page,
        )
