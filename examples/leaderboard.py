from unbelievaboat import Client
import asyncio


async def main():
    client = Client(...)

    guild_id = ...
    pages_to_fetch = ...

    leaderboard_users = []
    for page in range(pages_to_fetch):
        leaderboard = await client.get_guild_leaderboard(
            guild_id, params={"page": page + 1}
        )
        leaderboard_users.extend(leaderboard.users)
        if leaderboard.total_pages >= page:
            break

    print(leaderboard_users)

    await client.close()


asyncio.run(main())
