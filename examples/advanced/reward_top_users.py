import asyncio

from unbelievaboat import Client


async def main() -> None:
    client = Client(...)

    guild_id = ...
    item_id = ...

    # Fetch guild
    guild = await client.get_guild(guild_id)

    # Fetch leaderboard, by default it will fetch 1000 users
    leaderboard = await guild.get_leaderboard()  # limit=1000
    print(len(leaderboard.users))

    # Or fetch whole leaderboard
    leaderboard = await guild.get_full_leaderboard()
    print(len(leaderboard.users))

    # Add item & money to the leaderboard users
    tasks = []
    for user in leaderboard.users:
        tasks.append(guild.add_inventory_item(user.id, item_id, 1))
        tasks.append(user.update(cash=1000))
    await asyncio.gather(*tasks)

    await client.close()


asyncio.run(main())
