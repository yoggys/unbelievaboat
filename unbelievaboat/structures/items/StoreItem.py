from datetime import datetime

from .BaseItem import BaseItem


class StoreItem(BaseItem):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.id: str = data["id"]
        self.price: int = int(data["price"])
        self.is_inventory: bool = data["is_inventory"]
        self.stock_remaining: int = data["stock_remaining"]
        self.unlimited_stock: bool = data["unlimited_stock"]
        self.expires_at: datetime = (
            datetime.strptime(data["expires_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            if data.get("expires_at")
            else None
        )

    def __str__(self) -> str:
        return "<StoreItem id={} price={} is_inventory={} stock_remaining={} unlimited_stock={} expires_at={}>".format(
            self.id,
            self.price,
            self.is_inventory,
            self.stock_remaining,
            self.unlimited_stock,
            self.expires_at,
        )
