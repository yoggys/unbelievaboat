import asyncio

from unbelievaboat import Client


async def main() -> None:
    client = Client(...)

    guild_id = ...
    user_id = ...

    # Get user balance
    balance = await client.get_user_balance(guild_id, user_id)
    print(balance.cash, balance.bank, balance.total)

    # or use the Guild class
    guild = await client.get_guild(guild_id)
    balance = await guild.get_user_balance(user_id)
    print(balance.cash, balance.bank, balance.total)

    # Set bank & cash balance to 1000
    await balance.set(1000, 1000)
    print(balance.cash, balance.bank, balance.total)

    # Clear user balance
    balance = await balance.clear()
    print(balance.cash, balance.bank, balance.total)

    # Check the balance again but with request
    balance = await guild.get_user_balance(user_id)
    print(balance.cash, balance.bank, balance.total)

    await client.close()


asyncio.run(main())
