# UnbelievaBoat API Python Wrapper

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)

This is a Python wrapper for the UnbelievaBoat API, which provides access to the UnbelievaBoat Discord bot functionality. It allows you to interact with the API endpoints to retrieve guild information, user balances, leaderboard data, and more.

## Requirements

- Python 3.8 or higher

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


async def main():
    # Initialize the client with your API token
    client = Client("your-api-token")

    # Retrieve guild information
    guild = await client.get_guild(guild_id)
    print(guild)

    # Retrieve user balance
    user_balance = await client.get_user_balance(guild_id, user_id)
    print(user_balance)

    # Close the client session
    await client.close()


asyncio.run(main())
```

Replace `"your-api-token"` with your actual API token. You can obtain an API token by logging into the UnbelievaBoat dashboard and generating a token for your bot.

Please note that the above example demonstrates a basic usage scenario. You can explore other available methods in the `Client` class to interact with different API endpoints. You can also find more examples in the [examples](https://github.com/yoggys/unbelievaboat/tree/master/examples) directory.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/yoggys/unbelievaboat).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
