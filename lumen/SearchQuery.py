from enum import StrEnum
from typing import Optional, Self

from lumen.LumenAPIManager import LumenAPIManager
from lumen.SearchResult import SearchResult
from lumen.SearchTypes import Topic


class Sort(StrEnum):
    DateRecievedAsc = "date_received asc"
    DateReceivedDesc = "date_received desc"
    RelevancyAsc = "relevancy asc"
    RelevancyDesc = "relevancy desc"


class SearchQuery:

    def __init__(self, manager: LumenAPIManager):
        """Start a search query. Add parameters with functions and search
            with the .search() function."""
        self.manager = manager
        self.params: dict[str, str] = {}

    def with_query(self,
                   term: str,
                   term_require_all: Optional[bool] = None) -> Self:
        """The full-text query term, searches across all fields. By default,
        terms are joined with OR - to enforce that all terms in the term query
        must be in the noice to be a match, set term_require_all to True."""
        self.params.update({
            "term": term,
        })

        if term_require_all:
            self.params.update(
                {"term-require-all": str(term_require_all).lower()})

        return self

    def with_title(self,
                   title: str,
                   title_require_all: Optional[bool] = None) -> Self:
        """Search in the title field. To require all words to match, set
        require_all to True."""
        self.params.update({
            "title": title,
        })

        if title_require_all:
            self.params.update(
                {"title-require-all": str(title_require_all).lower()})

        return self

    def with_topic(self,
                   topic: Topic,
                   topic_require_all: Optional[bool] = None) -> Self:
        """Search in the topic field. To require all words to match, set
        require_all to True."""
        self.params.update({
            "topics": topic,
        })

        if topic_require_all:
            self.params.update(
                {"topics-require-all": str(topic_require_all).lower()})

        return self

    def with_tags(self,
                  tags: str,
                  tags_require_all: Optional[bool] = None) -> Self:
        """Search in the tags field. To require all words to match, set
        require_all to True."""
        self.params.update({
            "tags": tags,
        })

        if tags_require_all:
            self.params.update(
                {"tags-require-all": str(tags_require_all).lower()})

        return self

    def with_jurisdictions(
            self,
            jurisdictions: str,
            jurisdictions_require_all: Optional[bool] = None) -> Self:
        """Search in the jurisdictions field. To require all words to match, set
        require_all to True."""
        self.params.update({
            "jurisdictions": jurisdictions,
        })

        if jurisdictions_require_all:
            self.params.update({
                "jurisdictions-require-all":
                str(jurisdictions_require_all).lower()
            })

        return self

    def with_sender(self,
                    sender: str,
                    sender_require_all: Optional[bool] = None) -> Self:
        """Search in the sender's name. Note - this is the person who filed
        the request, not necessairly the content owner! To require all words to
        match, set require_all to True."""
        self.params.update({
            "sender_name": sender,
        })

        if sender_require_all:
            self.params.update(
                {"sender_name-require-all": str(sender_require_all).lower()})

        return self

    def with_principal(self,
                       principal: str,
                       principal_require_all: Optional[bool] = None) -> Self:
        """Search in the principal's name. Note - this is the organization
        that owns the content! I think. To require all words to match, set
        require_all to True."""
        self.params.update({
            "principal_name": principal,
        })

        if principal_require_all:
            self.params.update({
                "principal_name-require-all":
                str(principal_require_all).lower()
            })

        return self

    def with_recipient(self,
                       recipient: str,
                       recipient_require_all: Optional[bool] = None) -> Self:
        """Search in the receipient's name.  To require all words to match, set
        require_all to True."""
        self.params.update({
            "recipient_name": recipient,
        })

        if recipient_require_all:
            self.params.update({
                "recipient_name-require-all":
                str(recipient_require_all).lower()
            })

        return self

    def with_works_desc(self,
                        works_desc: str,
                        works_require_all: Optional[bool] = None) -> Self:
        """Search in the work's description.  To require all words to match, set
        require_all to True."""
        self.params.update({
            "works": works_desc,
        })

        if works_require_all:
            self.params.update(
                {"works-require-all": str(works_require_all).lower()})

        return self

    def with_action_taken(self, action_taken: str) -> Self:
        """Search based on the action taken on a notice."""
        self.params.update({"action_taken": action_taken})

        return self

    def with_amount(self, num_of_entries: int) -> Self:
        """Set the amount of results you will get. Cannot go past 10000."""
        if num_of_entries > 10000:
            # Todo: We can paginate (request a page of 10000 entries, then
            # the next page of 10000 entries, etc)
            raise Exception("Requested too many entries!")
        self.params.update({"per_page": str(num_of_entries)})
        return self
    
    def with_page(self, page: int) -> Self:
        """Set the page you want. This also depends on the amount of entries per
        page!"""
        self.params.update({"page": str(page)})
        return self

    def with_order(self, sort: Sort) -> Self:
        """Sorts the entries. (RelevancyDesc is the default option.)"""
        self.params.update({"sort_by": sort})
        return self

    # TODO: facet country code, date, language

    def search(self) -> SearchResult:
        if len(self.params) == 0:
            raise Exception("No search parameters!")
        data = self.manager._req("/notices/search.json", self.params)
        return SearchResult(data)
