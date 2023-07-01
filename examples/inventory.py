from unbelievaboat import Client
import asyncio


async def main():
    client = Client(...)

    guild_id = ...
    user_id = ...

    user = await client.get_inventory_items(guild_id, user_id)
    print(user.items)

    store = await client.get_store_items(guild_id)
    for item in store.items:
        user = await user.add_item(item, 1)
    print(user.items)

    while len(user.items) > 0:
        item = user.items[0]
        user = await user.remove_item(item, item.quantity)

    await client.close()


asyncio.run(main())
