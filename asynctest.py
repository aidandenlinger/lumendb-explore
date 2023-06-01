import asyncio
import logging
from os import getenv
from pathlib import Path
from pprint import pprint

from dotenv import load_dotenv
from lumen.AsyncLumenAPIManager import AsyncLumenAPIManager
from lumen.PaginatedSearchQuery import PaginatedSearchQuery

logging.basicConfig(level=logging.INFO)  # Comment out if you don't want logs

# Get our lumen API key from a .env file. DO NOT EVER PUSH THE KEY TO GITHUB
load_dotenv()
api_key = getenv("LUMEN_API")
if not api_key:
    print("A Lumen API key needs to be in a .env file, please see the README")
    exit(1)

# Actually start using the API!
async def main():
    async with AsyncLumenAPIManager(api_key, cache=Path("async_cache")) as api:
        notices = await PaginatedSearchQuery(api).with_amount_per_page(50).with_query("Skinamarink").with_page_range(1, 4).search()
        print([(notice.title, notice.date_received) for notice in notices])

asyncio.run(main())
