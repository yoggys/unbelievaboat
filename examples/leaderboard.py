import asyncio

from unbelievaboat import Client


async def main():
    client = Client(...)

    guild_id = ...
    pages_to_fetch = ...

    # Create a list for users
    leaderboard_users = []

    # Populate the list with leaderboard users
    for page in range(pages_to_fetch):
        leaderboard = await client.get_guild_leaderboard(guild_id, page=page + 1)
        leaderboard_users.extend(leaderboard.users)
        if not leaderboard.total_pages or leaderboard.total_pages >= page:
            break
    print(leaderboard_users)

    # or fetch whole leaderboard at once
    leaderboard = await client.get_full_guild_leaderboard(guild_id)
    print(leaderboard.users)

    await client.close()


asyncio.run(main())
