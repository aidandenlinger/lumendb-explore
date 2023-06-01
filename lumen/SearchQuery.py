import sys
from datetime import date, datetime
from typing import Dict, Optional

from lumen.AsyncLumenAPIManager import AsyncLumenAPIManager
from lumen.LumenAPIManager import LumenAPIManager
from lumen.SearchResult import SearchResult
from lumen.SearchTypes import Topic

if sys.version_info >= (3, 11):
    from enum import StrEnum
    from typing import Self
else:
    from strenum import StrEnum
    from typing_extensions import Self


class Sort(StrEnum):
    DateRecievedAsc = "date_received asc"
    DateReceivedDesc = "date_received desc"
    RelevancyAsc = "relevancy asc"
    RelevancyDesc = "relevancy desc"


class SearchQueryCore:

    def __init__(self) -> None:
        """Start a search query. Add parameters with functions and search
            with the .search() function."""
        self.params: Dict[str, str] = {}

    def _set_param_and_require_all(self, key: str, val: str,
                                   require_all: Optional[bool]) -> Self:
        self.params[key] = val

        if require_all is not None:
            self.params[key + "-require-all"] = str(require_all).lower()

        return self

    def with_query(self,
                   term: str,
                   term_require_all: Optional[bool] = None) -> Self:
        """The full-text query term, searches across all fields. By default,
        terms are joined with OR - to enforce that all terms in the term query
        must be in the noice to be a match, set term_require_all to True."""
        return self._set_param_and_require_all("term", term, term_require_all)

    def with_title(self,
                   title: str,
                   title_require_all: Optional[bool] = None) -> Self:
        """Search in the title field. To require all words to match, set
        require_all to True."""
        return self._set_param_and_require_all("title", title,
                                               title_require_all)

    def with_topic(self,
                   topic: Topic,
                   topic_require_all: Optional[bool] = None) -> Self:
        """Search in the topic field. To require all words to match, set
        require_all to True."""
        return self._set_param_and_require_all("topics", topic,
                                               topic_require_all)

    def with_tags(self,
                  tags: str,
                  tags_require_all: Optional[bool] = None) -> Self:
        """Search in the tags field. To require all words to match, set
        require_all to True."""
        return self._set_param_and_require_all("tags", tags, tags_require_all)

    def with_jurisdictions(
            self,
            jurisdictions: str,
            jurisdictions_require_all: Optional[bool] = None) -> Self:
        """Search in the jurisdictions field. To require all words to match, set
        require_all to True."""
        return self._set_param_and_require_all("jurisdictions", jurisdictions,
                                               jurisdictions_require_all)

    def with_sender(self,
                    sender: str,
                    sender_require_all: Optional[bool] = None) -> Self:
        """Search in the sender's name. Note - this is the person who filed
        the request, not necessairly the content owner! To require all words to
        match, set require_all to True."""
        return self._set_param_and_require_all("sender_name", sender,
                                               sender_require_all)

    def with_principal(self,
                       principal: str,
                       principal_require_all: Optional[bool] = None) -> Self:
        """Search in the principal's name. Note - this is the organization
        that owns the content! I think. To require all words to match, set
        require_all to True."""
        return self._set_param_and_require_all("principal_name", principal,
                                               principal_require_all)

    def with_recipient(self,
                       recipient: str,
                       recipient_require_all: Optional[bool] = None) -> Self:
        """Search in the receipient's name.  To require all words to match, set
        require_all to True."""
        return self._set_param_and_require_all("recipient_name", recipient,
                                               recipient_require_all)

    def with_works_desc(self,
                        works_desc: str,
                        works_require_all: Optional[bool] = None) -> Self:
        """Search in the work's description.  To require all words to match, set
        require_all to True."""
        return self._set_param_and_require_all("works", works_desc,
                                               works_require_all)

    def with_action_taken(self, action_taken: str) -> Self:
        """Search based on the action taken on a notice."""
        self.params["action_taken"] = action_taken

        return self

    def with_amount(self, num_of_entries: int) -> Self:
        """Set the amount of results you will get. Cannot go past 10000."""
        if num_of_entries > 10000:
            # Todo: We can paginate (request a page of 10000 entries, then
            # the next page of 10000 entries, etc)
            raise Exception("Requested too many entries!")
        self.params["per_page"] = str(num_of_entries)
        return self

    def with_page(self, page: int) -> Self:
        """Set the page you want. This also depends on the amount of entries per
        page!"""
        self.params["page"] = str(page)
        return self

    def with_order(self, sort: Sort) -> Self:
        """Sorts the entries. (RelevancyDesc is the default option.)"""
        self.params["sort_by"] = sort
        return self

    def with_date_range(self, d1: date, d2: date) -> Self:
        """The date range. Asssumes you don't care about hours
        or seconds, just dates."""
        if (d1 > d2):
            raise Exception("Start date is after end date!")

        def to_epoch(d: date) -> int:
            # We have to add hours and minutes, use min.time() to get and combine
            # Lumen wants a timestamp in *milliseconds*, so we multiply by 1000
            return int(
                datetime.combine(d, datetime.min.time()).timestamp() * 1000)

        self.params["date_received_facet"] = f"{to_epoch(d1)}..{to_epoch(d2)}"
        return self

    # TODO: facet country code, language


class SearchQuery(SearchQueryCore):

    def __init__(self, manager: LumenAPIManager) -> None:
        super().__init__()
        self.manager = manager

    def search(self) -> SearchResult:
        if len(self.params) == 0:
            raise Exception("No search parameters!")
        data = self.manager._req("/notices/search.json", self.params)
        return SearchResult(data)


class AsyncSearchQuery(SearchQueryCore):

    def __init__(self, manager: AsyncLumenAPIManager) -> None:
        super().__init__()
        self.manager = manager

    async def search(self) -> SearchResult:
        if len(self.params) == 0:
            raise Exception("No search parameters!")
        data = await self.manager._req("/notices/search.json", self.params)
        return SearchResult(data)

    def copy(self) -> Self:
        new = self.__class__(self.manager)
        new.params = self.params.copy()
        return new
