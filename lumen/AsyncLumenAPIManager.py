import json
import logging
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx


class AsyncLumenAPIManager:
    """Manage requests to the Lumen database and timing requests."""

    def __init__(self,
                 api_key: str,
                 cache: Optional[Path] = Path("cache")):
        headers = {
            "User-Agent": "CSE291BResearch",
            "X-Authentication-Token": api_key,
            "Accept-Encoding": "gzip"
        }
        self.session = httpx.AsyncClient(headers=headers, timeout=None)
        self.cache = cache
        if self.cache:
            self.cache.mkdir(exist_ok=True)

    async def __aenter__(self):
        """Start the session using a with-context block."""
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        """Exit a with-context block."""
        await self.close()

    async def close(self):
        """Close the requests session."""
        await self.session.aclose()

    async def get_notice(self, id: int) -> Dict[str, Any]:
        """Return a JSON-encoded representation of selected notice attributes.
        Notice Types will have mapped attributes applied, and be under a root
        key articulating their type."""
        return await self._req(f"/notices/{id}.json")

    async def get_topics(self) -> List[Any]:
        """Return a JSON-encoded array of topics, including an id, name, and
        parent_id."""
        data = await self._req("/topics.json")
        return data['topics']

    async def search_entity(self,
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

        return await self._req("/entities/search.json", params=params)

    async def _req(self,
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

        logging.info(f"Requesting {path} with params {params}")
        req = await self.session.get("https://lumendatabase.org" + path,
                                     params=params)
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
