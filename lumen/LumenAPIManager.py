import logging
from datetime import datetime
from time import sleep
from typing import Any, Optional

import requests


class LumenAPIManager:
    """Manage requests to the Lumen database and timing requests."""

    def __init__(self, api_key: str, timeout: int = 2):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "CSE291BResearch",
            "X-Authentication-Token": api_key,
            "Accept-Encoding": "gzip"
        })
        self.last_req: datetime | None = None
        self.timeout = timeout

    def __enter__(self):
        """Start the session using a with-context block."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Exit a with-context block."""
        self.close()

    def close(self):
        """Close the requests session."""
        self.session.close()

    def get_notice(self, id: int) -> dict[str, Any]:
        """Return a JSON-encoded representation of selected notice attributes.
        Notice Types will have mapped attributes applied, and be under a root
        key articulating their type."""
        return self._req(f"/notices/{id}.json")

    def get_topics(self) -> list[Any]:
        """Return a JSON-encoded array of topics, including an id, name, and
        parent_id."""
        data = self._req("/topics.json")
        return data['topics']

    def search_entity(self,
                      entity_name: str,
                      page: Optional[int] = None,
                      per_page: Optional[int] = None) -> dict[str, Any]:
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
             params: Optional[dict[str, str]] = None) -> dict[str, Any]:
        """Make a request on the path on the lumen database."""
        self._wait()

        logging.info(f"Requesting {path} with params {params}")
        req = self.session.get("https://lumendatabase.org" + path,
                               params=params)
        self.last_req = datetime.now()
        req.raise_for_status()  # Raises exception on error

        return req.json()

    def _wait(self):
        """Ensure that we only make one request per second."""
        if not self.last_req:
            # No requests have been made
            return

        req_delta = (datetime.now() - self.last_req).total_seconds()

        if req_delta < self.timeout:
            logging.info(f"Sleeping for {self.timeout} seconds")
            sleep(self.timeout)
