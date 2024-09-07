import asyncio

from unbelievaboat import Client


async def main() -> None:
    client = Client(...)

    guild_id = ...
    pages_to_fetch = ...

    # Create a list for items
    store_items = []

    # Populate the list with guild items
    for page in range(pages_to_fetch):
        store = await client.get_store_items(guild_id, page=page + 1)
        store_items.extend(store.items)
        if store.total_pages >= page:
            break
    print(store_items)

    # or fetch all items at once
    store = await client.get_all_store_items(guild_id)
    print(store.items)

    await client.close()


asyncio.run(main())
