from typing import Any, Dict, Optional, Self


class User:
    def __init__(self, client, data: Dict[str, Any] = {}) -> None:
        self.guild_id: str = data.get("guild_id")
        self.user_id: str = data.get("user_id")
        self.rank: Optional[int] = data.get("rank")
        self.cash: int = data.get("cash")
        self.bank: int = data.get("bank")
        self.total: int = data.get("total")

        self._client = client
        self._raw_data: Dict[str, Any] = data

    def __str__(self) -> str:
        return "<User id={} guild_id={} rank={} cash={} bank={} total={}>".format(
            self.id, self.guild_id, self.rank, self.cash, self.bank, self.total
        )

    @property
    def id(self) -> str:
        return self.user_id

    async def set_balance(self, data: Dict[str, Any] = {}, reason: str = None) -> Self:
        self = await self._client.set_user_balance(
            self.guild_id, self.user_id, data, reason
        )
        return self

    async def update_balance(
        self, data: Dict[str, Any] = {}, reason: str = None
    ) -> Self:
        self = await self._client.edit_user_balance(
            self.guild_id, self.user_id, data, reason
        )
        return self
