from typing import Optional


class User:
    def __init__(self, data: dict = {}) -> None:
        self.rank: Optional[int] = data.get("rank")
        self.user_id: str = data.get("user_id")
        self.cash: int = data.get("cash")
        self.bank: int = data.get("bank")
        self.total: int = data.get("total")
        self._raw_data: dict = data

    @property
    def id(self) -> str:
        return self.user_id

    def __str__(self) -> str:
        return "<User id={} cash={} bank={} total={}>".format(
            self.id, self.cash, self.bank, self.total
        )
