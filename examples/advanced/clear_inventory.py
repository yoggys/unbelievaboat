import asyncio

from unbelievaboat import Client


async def main() -> None:
    client = Client(...)

    guild_id = ...
    user_id = ...

    # Get user inventory
    inventory = await client.get_inventory_items(guild_id, user_id)

    # Remove items from user inventory one by one
    tasks = [inventory.remove(item, item.quantity) for item in inventory.items]
    await asyncio.gather(*tasks)

    # Or remove items using inventory helper methods
    await inventory.clear()

    await client.close()


asyncio.run(main())
