from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from typing_extensions import Self


class Embed:
    # noinspection PyUnusedLocal
    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[int] = None,
        fields: Optional[Dict[str, Any]] = None,
        author: Optional[Dict[str, str]] = None,
        footer: Optional[Dict[str, str]] = None,
        timestamp: Optional[datetime] = None,
        image: Optional[Dict[str, str]] = None,
        thumbnail: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> None:
        self.title: str = title
        self.description: str = description
        self.color: int = color
        self.fields: Optional[List[Dict[str, Union[str, bool]]]] = fields or []
        self.author: Optional[Dict[str, str]] = author
        self.footer: Optional[Dict[str, str]] = footer
        self.timestamp: Optional[datetime] = timestamp
        self.image: Optional[Dict[str, str]] = image
        self.thumbnail: Optional[Dict[str, str]] = thumbnail

    def __str__(self) -> str:
        return "<Embed title='{}' description='{}' color={} fields={} author={} footer={} timestamp='{}' image={} thumbnail={}>".format(
            self.title,
            self.description,
            self.color,
            self.fields,
            self.author,
            self.footer,
            self.timestamp,
            self.image,
            self.thumbnail,
        )

    def json(self) -> Dict[str, Any]:
        json = {}
        if self.title:
            json["title"] = self.title
        if self.description:
            json["description"] = self.description
        if self.color:
            json["color"] = self.color
        if self.fields:
            json["fields"] = self.fields
        if self.author:
            json["author"] = self.author
        if self.footer:
            json["footer"] = self.footer
        if self.timestamp:
            json["timestamp"] = self.timestamp.isoformat()
        if self.image:
            json["image"] = self.image
        if self.thumbnail:
            json["thumbnail"] = self.thumbnail
        return json

    def set_footer(self, text: str, icon_url: Optional[str] = None) -> Self:
        footer = {"text": text}
        if icon_url is not None:
            footer["icon_url"] = icon_url
        self.footer = footer
        return self

    def set_author(
        self, name: str, url: Optional[str] = None, icon_url: Optional[str] = None
    ) -> Self:
        author = {"name": name}
        if url is not None:
            author["url"] = url
        if icon_url is not None:
            author["icon_url"] = icon_url
        self.author = author
        return self

    def add_field(self, name: str, value: str, inline: bool = True) -> None:
        self.fields.append({"name": name, "value": value, "inline": inline})

    def set_image(self, url: str) -> Self:
        self.image = {"url": url}
        return self

    def set_thumbnail(self, url: str) -> Self:
        self.thumbnail = {"url": url}
        return self
