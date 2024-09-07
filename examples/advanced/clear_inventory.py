import asyncio

from unbelievaboat import Client


async def main() -> None:
    client = Client(...)

    guild_id = ...
    user_id = ...

    # Get user inventory
    inventory = await client.get_inventory_items(guild_id, user_id)

    # Get guild store
    store = await client.get_all_store_items(guild_id)

    # Remove inventory items that are not in store
    store_ids = [item.id for item in store.items]
    for item in inventory.items:
        if item.id not in store_ids:
            # Use any of below methods to clear item from inventory
            await inventory.remove(item, item.quantity)
            await inventory.clear(item)
            await item.clear()

    # Remove items from user inventory one by one
    tasks = [inventory.remove(item, item.quantity) for item in inventory.items]
    await asyncio.gather(*tasks)

    # Or remove all items using simple inventory helper method
    await inventory.clear()

    await client.close()


asyncio.run(main())
