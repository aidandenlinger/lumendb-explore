import logging
from os import getenv

from dotenv import load_dotenv

from lumen.LumenAPIManager import LumenAPIManager

logging.basicConfig(level=logging.INFO)  # Comment out if you don't want logs

load_dotenv()
api_key = getenv("LUMEN_API")
if not api_key:
    print("A Lumen API key needs to be in a .env file, please see the README")
    exit(1)

with LumenAPIManager(api_key) as api:
    print(api.get_notice(1))
    print(api.get_notice(2))
