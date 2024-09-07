from typing import Dict


class Permission:
    def __init__(self, guild_id: int, allow: int) -> None:
        self.guild_id: int = int(guild_id)
        self.allow: int = allow

    def __str__(self) -> str:
        return "<Permission allow={}, economy={}, items={}>".format(
            self.allow, self.economy, self.items
        )

    @property
    def id(self) -> int:
        return self.guild_id

    @property
    def economy(self) -> bool:
        return bool(self.allow & 0x00000001)  # (1 << 0)

    @property
    def items(self) -> bool:
        return bool(self.allow & 0x00000002)  # (1 << 1)

    def json(self) -> Dict[str, bool]:
        return {"economy": self.economy, "items": self.items}
