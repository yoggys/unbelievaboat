from unbelievaboat import Client
import asyncio


async def main():
    client = Client(...)

    guild_id = ...
    user_id = ...

    user = await client.get_user_balance(guild_id, user_id)

    print(user.id)
    print(user.bank)
    print(user.cash)
    print(user.total)

    await client.close()


asyncio.run(main())
