import asyncio

from unbelievaboat import Client


async def main():
    client = Client(...)

    guild_id = ...

    # Get guild permissions
    permissions = await client.get_application_permission(guild_id)

    # Check permissions
    print(permissions.allow)
    print(permissions.economy)
    print(permissions.items)

    await client.close()


asyncio.run(main())
