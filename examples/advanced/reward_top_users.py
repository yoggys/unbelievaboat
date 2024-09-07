import asyncio

from unbelievaboat import Client


async def main():
    client = Client(...)

    guild_id = ...
    item_id = ...

    # Fetch guild leaderboard, by default it will fetch 1000 users
    leaderboard = await client.get_guild_leaderboard(guild_id)  # {"limit": ...}

    # Or fetch whole leaderboard
    leaderboard = await client.get_guild_leaderboard_all(guild_id)

    # Add items to the leaderboard users
    tasks = [
        client.add_inventory_item(guild_id, user.id, {"item_id": item_id, "quanity": 1})
        for user in leaderboard.users
    ]
    await asyncio.gather(*tasks)

    await client.close()


asyncio.run(main())
