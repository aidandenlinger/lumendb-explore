import logging
from os import getenv
from pprint import pprint

from dotenv import load_dotenv

from lumen.LumenAPIManager import LumenAPIManager
from lumen.SearchQuery import SearchQuery, Topic

logging.basicConfig(level=logging.INFO)  # Comment out if you don't want logs

# Get our lumen API key from a .env file. DO NOT EVER PUSH THE KEY TO GITHUB
load_dotenv()
api_key = getenv("LUMEN_API")
if not api_key:
    print("A Lumen API key needs to be in a .env file, please see the README")
    exit(1)

# Actually start using the API!
with LumenAPIManager(api_key) as api:
    # Entity (people who file requests) and notice grabbing is basic for now
    # Note that we can make multiple API requests at a time - the manager will
    # take care of sleeping between requests
    pprint(api.search_entity("Youtube Inc", per_page=1))
    pprint(api.get_notice(5))

    # Searching is more fleshed out, as that's what we'll be doing.
    # Create a new search query, add all the terms you want, and then search.
    # You'll get a SearchResult back!
    # Let's get the first 5 Star Wars results.
    result = SearchQuery(api).with_query("star wars").with_amount(
        5).with_topic(Topic.DMCANotice).search()

    # First, we can look at the metadata. This is pretty powerful by itself -
    # without having to get every single notice, we get plenty of numbers about
    # *every* entry that applied to our term. For instance, who are the top 10
    # principals for Star Wars content?
    print(
        f"The top 10 requesters for Star Wars content (in these requests) are: {result.metadata.principals}"
    )
    
    # More examples in the Jupyter notebook
    
    # Since this is in a "with" block, the session will close itself :)
