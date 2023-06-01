import json
import logging
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from time import sleep
from typing import Any, Dict, List, Optional, Union

import httpx


class LumenAPIManager:
    """Manage requests to the Lumen database and timing requests."""

    def __init__(self,
                 api_key: str,
                 cache: Optional[Path] = Path("cache"),
                 timeout: int = 2):
        headers = {
            "User-Agent": "CSE291BResearch",
            "X-Authentication-Token": api_key,
            "Accept-Encoding": "gzip"
        }
        self.session = httpx.Client(headers=headers, timeout=None)
        self.last_req: Union[datetime, None] = None
        self.timeout = timeout
        self.cache = cache
        if self.cache:
            self.cache.mkdir(exist_ok=True)

    def __enter__(self):
        """Start the session using a with-context block."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Exit a with-context block."""
        self.close()

    def close(self):
        """Close the requests session."""
        self.session.close()

    def get_notice(self, id: int) -> Dict[str, Any]:
        """Return a JSON-encoded representation of selected notice attributes.
        Notice Types will have mapped attributes applied, and be under a root
        key articulating their type."""
        return self._req(f"/notices/{id}.json")

    def get_topics(self) -> List[Any]:
        """Return a JSON-encoded array of topics, including an id, name, and
        parent_id."""
        data = self._req("/topics.json")
        return data['topics']

    def search_entity(self,
                      entity_name: str,
                      page: Optional[int] = None,
                      per_page: Optional[int] = None) -> Dict[str, Any]:
        """Return a JSON-encoded hash including an array of entities and
        metadata about the search results."""
        params = {"term": entity_name}
        if page:
            params['page'] = str(page)
        if per_page:
            params['per_page'] = str(per_page)

        return self._req("/entities/search.json", params=params)

    def _req(self,
             path: str,
             params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make a request on the path on the lumen database (or load from cache)."""
        key = {}
        if params:
            key.update(params)
        key['path'] = path
        hash_key = sha256(json.dumps(key, sort_keys=True).encode()).hexdigest()

        if self.cache:
            # Try loading from cache
            cache_path = self.cache / f"{hash_key}.json"
            try:
                with cache_path.open() as input:
                    logging.info(
                        f"Cache hit on {path} with {params} at {cache_path}")
                    return json.load(input)
            except FileNotFoundError:
                # File was not found, continue to make api request
                pass

        # Not in cache (or no cache), make a request
        self._wait()

        logging.info(f"Requesting {path} with params {params}")
        req = self.session.get("https://lumendatabase.org" + path,
                               params=params)
        self.last_req = datetime.now()
        req.raise_for_status()  # Raises exception on error
        req_json = req.json()

        # Save to cache
        if self.cache:
            with cache_path.open("w+") as output:
                logging.info(f"Caching at {cache_path}")
                json.dump(req_json, output)
            with (self.cache / f"{hash_key}.metadata").open("w+") as output:
                json.dump(key, output, sort_keys=True, indent=2)

        return req_json

    def _wait(self):
        """Ensure that we only make one request per second."""
        if not self.last_req:
            # No requests have been made
            return

        req_delta = (datetime.now() - self.last_req).total_seconds()

        if req_delta < self.timeout:
            logging.info(f"Sleeping for {self.timeout} seconds")
            sleep(self.timeout)
