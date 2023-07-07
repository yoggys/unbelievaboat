from unbelievaboat import Client
import asyncio


async def main():
    client = Client(...)

    guild_id = ...
    user_id = ...

    # Get user balance
    balance = await client.get_user_balance(guild_id, user_id)
    print(balance.total)

    # Clear user balance
    balance = await balance.clear_balance()
    print(balance.total)

    await client.close()


asyncio.run(main())
