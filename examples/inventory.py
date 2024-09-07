import asyncio

from unbelievaboat import Client


async def main() -> None:
    client = Client(...)

    guild_id = ...
    user_id = ...

    # Get user inventory
    inventory = await client.get_inventory_items(guild_id, user_id)
    print(inventory.items)

    # Get guild store
    store = await client.get_store_items(guild_id)

    # Add each item from the store to the user inventory
    for item in store.items:
        await inventory.add(item, 1)
    print(inventory.items)

    # Remove each item from the user inventory
    while len(inventory.items) > 0:
        item = inventory.items[0]
        await inventory.remove(item, item.quantity)

    # or just use helper function
    await inventory.clear()

    await client.close()


asyncio.run(main())
