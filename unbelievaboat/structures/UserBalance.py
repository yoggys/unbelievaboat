from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from typing_extensions import Self

from ..utils import MISSING

if TYPE_CHECKING:
    from ..Client import Client


class UserBalance:
    def __init__(self, client: "Client", data: Dict[str, Any]) -> None:
        self.guild_id: int = int(data.get("guild_id"))
        self.user_id: int = int(data.get("user_id"))
        self.rank: Optional[int] = data.get("rank")
        self.cash: int = data.get("cash")
        self.bank: int = data.get("bank")
        self.total: int = data.get("total")

        self._client: "Client" = client
        self._raw_data: Dict[str, Any] = data

    def __str__(self) -> str:
        return (
            "<UserBalance id={} guild_id={} rank={} cash={} bank={} total={}>".format(
                self.id, self.guild_id, self.rank, self.cash, self.bank, self.total
            )
        )

    @property
    def id(self) -> int:
        return self.user_id

    def _update(self, data: Self) -> None:
        self.rank = data.rank
        self.cash = data.cash
        self.bank = data.bank
        self.total = data.total

    async def refresh(self) -> Self:
        self._update(await self._client.get_user_balance(self.guild_id, self.user_id))
        return self

    async def set(
        self, cash: int = MISSING, bank: int = MISSING, reason: str = None
    ) -> Self:
        self._update(
            await self._client.set_user_balance(
                self.guild_id, self.user_id, cash, bank, reason
            )
        )
        return self

    async def update(
        self, cash: int = MISSING, bank: int = MISSING, reason: str = None
    ) -> Self:
        self._update(
            await self._client.update_user_balance(
                self.guild_id, self.user_id, cash, bank, reason
            )
        )
        return self

    async def clear(self, reason: str = None) -> Self:
        self._update(
            await self._client.set_user_balance(
                self.guild_id, self.user_id, cash=0, bank=0, reason=reason
            )
        )
        return self
