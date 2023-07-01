from unbelievaboat import Client
import asyncio


async def main():
    client = Client(...)

    guild_id = ...
    pages_to_fetch = ...

    store_items = []
    for page in range(pages_to_fetch):
        store = await client.get_store_items(guild_id, params={"page": page + 1})
        store_items.extend(store.items)
        if store.total_pages >= page:
            break
    print(store_items)

    await client.close()


asyncio.run(main())
