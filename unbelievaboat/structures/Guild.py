from typing import Any, Dict, Optional


class Guild:
    def __init__(self, data: Dict[str, Any] = {}) -> None:
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.icon: Optional[str] = data.get("icon")
        self.owner_id: str = data.get("owner_id")
        self.member_count: int = data.get("member_count")
        self.currency_symbol: str = data.get("symbol")
        self._raw_data: Dict[str, Any] = data

    def __str__(self) -> str:
        return "<Guild id={} name='{}' owner_id={} member_count={}>".format(
            self.owner_id, self.name, self.owner_id, self.member_count
        )

    @property
    def icon_url(self) -> Optional[str]:
        if self.icon:
            extension = "gif" if self.icon.startswith("a_") else "png"
            return f"https://cdn.discordapp.com/icons/{self.id}/{self.icon}.{extension}"
        return None
