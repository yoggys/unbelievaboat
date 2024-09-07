import asyncio

from unbelievaboat import Client


async def main():
    client = Client(...)

    guild_id = ...

    # Get guild information
    guild = await client.get_guild(guild_id)

    print(guild.id)
    print(guild.name)
    print(guild.owner_id)
    print(guild.icon_url)
    print(guild.currency_symbol)

    await client.close()


asyncio.run(main())
