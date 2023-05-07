import asyncio
import os
from pdisk import Pdisk
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


async def account_info():
    api_key = os.environ.get("API")
    pdisk = Pdisk(api_key)
    account_info = await pdisk.account_info()
    print(account_info.email)  # string
    print(account_info.balance)  # float USD
    print(account_info.storage_used)  # None Or Float

asyncio.run(account_info())
