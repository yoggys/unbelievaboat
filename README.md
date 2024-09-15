# UnbelievaBoat API Python Wrapper

[![Discord Server](https://img.shields.io/discord/746360067632136222?label=discord&style=for-the-badge&logo=discord&color=5865F2&logoColor=white)](https://dc.yoggies.dev/)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-380/)
[![PyPI Version](https://img.shields.io/pypi/v/unbelievaboat.svg?style=for-the-badge&color=yellowgreen&logo=pypi&logoColor=white)](https://pypi.org/project/unbelievaboat/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/unbelievaboat?style=for-the-badge&color=blueviolet&logo=pypi&logoColor=white)](https://pypi.org/project/unbelievaboat/)

This is a Python wrapper for the UnbelievaBoat API, which provides access to the UnbelievaBoat Discord bot functionality. It allows you to interact with the API endpoints to retrieve guild information, user balances, leaderboard data, and more.

## Installation

You can install the UnbelievaBoat API Python wrapper using pip. Open your terminal and run the following command:

```shell
pip install unbelievaboat
```

## Usage

Here's an example of how to use the UnbelievaBoat API Python wrapper to interact with the UnbelievaBoat API:

```python
from unbelievaboat import Client
import asyncio


async def main() -> None:
    # Initialize the client with your API token
    client = Client("your-api-token")
    
    guild_id = ...
    user_id = ...

    # Retrieve guild information
    guild = await client.get_guild(guild_id)
    print(guild)

    # Retrieve user balance
    user = await guild.get_user_balance(user_id)
    print(user)
    
    # Set or update user balance
    await user.set(bank=100)
    await user.update(bank=-100)
    print(user)

    # Close the client session
    await client.close()
    
    # You can also use async context manager
    async with Client("your-api-token") as client:
        leaderboard = await client.get_guild_leaderboard(guild_id)
        print(leaderboard)
        
        
asyncio.run(main())
```

Replace `"your-api-token"` with your actual API token. You can obtain an API token by logging into the UnbelievaBoat dashboard and generating a token for your bot.

Please note that the above example demonstrates a basic usage scenario. You can explore other available methods in the `Client` class to interact with different API endpoints. You can also find more examples in the [examples](https://github.com/yoggys/unbelievaboat/tree/main/examples) directory. For more information about the UnbelievaBoat API (data/params), please refer to the [official documentation](https://unbelievaboat-api.readme.io/reference/).

## Requirements

- Python 3.8+

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/yoggys/unbelievaboat).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
