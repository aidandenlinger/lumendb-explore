import json
import logging
from os import getenv
from typing import Any

from dotenv import load_dotenv

from lumen.LumenAPIManager import LumenAPIManager

logging.basicConfig(level=logging.INFO)  # Comment out if you don't want logs

load_dotenv()
api_key = getenv("LUMEN_API")
if not api_key:
    print("A Lumen API key needs to be in a .env file, please see the README")
    exit(1)


def pprint(data: dict[str, Any]):
    """Pretty print JSON."""
    print(json.dumps(data, indent=2))


with LumenAPIManager(api_key) as api:
    print(api.get_topics())
    pprint(api.search_entity("Youtube Inc", per_page=5))
    pprint(api.get_notice(5))
