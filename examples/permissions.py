import asyncio

from unbelievaboat import Client


async def main() -> None:
    client = Client(...)

    guild_id = ...

    # Get guild permissions
    permissions = await client.get_application_permission(guild_id)

    # Check permissions
    print(f"Flags: {permissions}")
    print(f"Economy: {permissions.economy}")
    print(f"Items: {permissions.items}")

    await client.close()


asyncio.run(main())
