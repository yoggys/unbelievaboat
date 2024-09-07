import asyncio

from unbelievaboat import Client


async def main() -> None:
    client = Client(...)

    guild_id = ...
    user_id = ...

    # Get user balance
    balance = await client.get_user_balance(guild_id, user_id)
    print(balance.total)

    # or use the Guild class
    guild = await client.get_guild(guild_id)
    balance = await guild.get_user_balance(user_id)
    print(balance.total)

    # Clear user balance
    balance = await balance.clear()
    print(balance.total)

    await client.close()


asyncio.run(main())
