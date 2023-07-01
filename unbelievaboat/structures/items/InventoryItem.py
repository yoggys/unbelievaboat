from .BaseItem import BaseItem


class InventoryItem(BaseItem):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.item_id: str = data["item_id"]
        self.quantity: int = data["quantity"]

    def __str__(self) -> str:
        return "<InventoryItem item_id={} quantity={}>".format(
            self.item_id, self.quantity
        )
