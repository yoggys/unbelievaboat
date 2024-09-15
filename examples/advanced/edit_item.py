import asyncio

from unbelievaboat import (
    Client,
    Embed,
    ItemActionType,
    ItemRequirementMatchType,
    ItemRequirementType,
    Message,
    StoreItemAction,
    StoreItemRequirement,
)


async def main() -> None:
    client = Client(...)

    guild_id = ...
    item_id = ...
    role_ids = [..., ...]

    # Get store item
    item = await client.get_store_item(guild_id, item_id)
    print(item)

    # Create embed
    embed = Embed(title="Title", description="Description", color=5793266)
    embed.set_footer(text="text", icon_url="https://yoggies.dev/assets/logo.png")
    embed.set_image(url="https://yoggies.dev/assets/logo.png")
    embed.set_thumbnail(url="https://yoggies.dev/assets/logo.png")

    # Create message with content and embed
    message = Message("Content", [embed])

    # Edit item actions & requirements
    await item.edit(
        description="new description",
        actions=[
            StoreItemAction(type=ItemActionType.RESPOND, message=message),
        ],
        requirements=[
            StoreItemRequirement(
                type=ItemRequirementType.ROLE,
                match_type=ItemRequirementMatchType.AT_LEAST_ONE,
                ids=role_ids,
            )
        ],
    )
    print(item)

    await client.close()


asyncio.run(main())
