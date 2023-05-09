import logging
from datetime import datetime
from time import sleep
from typing import Any

import requests


class LumenAPIManager:

    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "CSE291BResearch",
            "X-Authentication-Token": api_key,
        }
        self.last_req: datetime | None = None

    def __enter__(self):
        """Start the session using a with-context block."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Close the requests session."""
        self.session.close()

    def get_notice(self, id: int) -> dict[str, Any]:
        """Return a JSON-encoded representation of selected notice attributes.
        Notice Types will have mapped attributes applied, and be under a root
        key articulating their type."""
        return self._req(f"/notices/{id}.json")

    def _req(self, path: str) -> dict[str, Any]:
        """Make a request on the path on the lumen database."""
        self._wait()

        logging.info(f"Requesting {path}")
        req = self.session.get("https://lumendatabase.org" + path,
                               headers=self.headers)
        self.last_req = datetime.now()
        req.raise_for_status()  # Raises exception on error

        return req.json()

    def _wait(self):
        """Ensure that we only make one request per second."""
        if not self.last_req:
            # No requests have been made
            return

        # sleeping for 1 was still giving me a timeout :(
        timeout_amt = 2

        req_delta = (datetime.now() - self.last_req).total_seconds()

        if req_delta < timeout_amt:
            logging.info(f"Sleeping for {timeout_amt} seconds")
            sleep(timeout_amt)
