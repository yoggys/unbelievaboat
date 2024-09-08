from typing import Any, Dict, List, Optional, Union

from typing_extensions import Self

from .Embed import Embed


class Message:
    # noinspection PyUnusedLocal
    def __init__(
        self,
        content: Optional[str] = None,
        embeds: Optional[List[Union[Embed, Dict[str, Any]]]] = None,
        **kwargs
    ) -> None:
        self.content: Optional[str] = content
        self.embeds: Optional[List[Embed]] = [
            embed if isinstance(embed, Embed) else Embed(**embed) for embed in embeds
        ] or []

        if not self.embeds and not self.content:
            raise ValueError("Either content or embed must be provided")

    def __str__(self) -> str:
        return "<Message content='{}' embeds={}>".format(
            self.content, [str(embed) for embed in self.embeds]
        )

    def add_embed(self, embed: Embed) -> Self:
        self.embeds.append(embed)
        return self

    def json(self) -> Dict[str, Any]:
        json = {}
        if self.content:
            json["content"] = self.content
        if self.embeds:
            json["embeds"] = [embed.json() for embed in self.embeds]
        return json
