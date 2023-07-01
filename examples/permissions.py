from unbelievaboat import Client
import asyncio


async def main():
    client = Client(...)

    guild_id = ...

    permissions = await client.get_application_permission(guild_id)
    print(permissions.allow)

    await client.close()


asyncio.run(main())
