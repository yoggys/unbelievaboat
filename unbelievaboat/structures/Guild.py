from typing import Optional


class Guild:
    def __init__(self, data: dict = {}) -> None:
        self.id: Optional[str] = data.get("id")
        self.name: Optional[str] = data.get("name")
        self.icon: Optional[str] = data.get("icon")
        self.owner_id: Optional[str] = data.get("owner_id")
        self.member_count: Optional[int] = data.get("member_count")
        self.currency_symbol: Optional[str] = data.get("symbol")
        self._raw_data: dict = data

    @property
    def icon_url(self) -> Optional[str]:
        if self.icon:
            extension = "gif" if self.icon.startswith("a_") else "png"
            return f"https://cdn.discordapp.com/icons/{self.id}/{self.icon}.{extension}"
        return None

    def __str__(self) -> str:
        return "<Guild id={} name='{}' owner_id={} member_count={}>".format(
            self.owner_id, self.name, self.owner_id, self.member_count
        )
