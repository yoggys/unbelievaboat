import asyncio

from unbelievaboat import Client


async def main():
    client = Client(...)

    guild_id = ...
    item_id = ...

    # Fetch guild leaderboard, by default it will fetch 1000 users
    leaderboard = await client.get_guild_leaderboard(guild_id)  # limit=1000
    print(len(leaderboard.users))

    # Or fetch whole leaderboard
    leaderboard = await client.get_full_guild_leaderboard(guild_id)
    print(len(leaderboard.users))

    # Add items to the leaderboard users
    tasks = [
        client.add_inventory_item(guild_id, user.id, item_id, 1)
        for user in leaderboard.users
    ]
    await asyncio.gather(*tasks)

    await client.close()


asyncio.run(main())
