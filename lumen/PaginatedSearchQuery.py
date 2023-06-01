import sys
from datetime import date
from typing import Optional

from lumen.LumenAPIManager import LumenAPIManager
from lumen.SearchQuery import SearchQuery, Sort
from lumen.SearchResult import Notice
from lumen.SearchTypes import Topic

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class PaginatedSearchQuery:

    def __init__(self, manager: LumenAPIManager):
        """Start a paginated search query. Add parameters with functions and search
            with the .search() function."""
        self.query = SearchQuery(manager)
        self.page_start = 1
        self.page_end = 1

    def with_amount_per_page(self, num_of_entries: int) -> Self:
        """Set the amount of results you will get per page. Cannot go past 10000."""
        self.query = self.query.with_amount(num_of_entries)
        return self

    def with_page_range(self, start: int, end: int) -> Self:
        """Set the page page you want. Both ends are inclusive, 
        so with_page_range(1,2) will get pages 1 and 2.
        This also depends on the amount of entries per page!"""
        if (start < 1):
            raise Exception("Cannot get pages lower than page 1!")
        if (start > end):
            raise Exception("End page is larger than start page!")

        self.page_start = start
        self.page_end = end
        return self

    # TODO: facet country code, language

    def search(self) -> list[Notice]:
        """Search and get the collected notices for the page range. Does not return
        metadata or the raw queries."""
        notices = []

        # Since page_end is inclusive, we need to add 1
        for page in range(self.page_start, self.page_end + 1):
            data = self.query.with_page(page).search()
            notices.extend(data.notices)

        return notices

    # Boilerplate, forwards calls to the inner query

    def with_query(self,
                   term: str,
                   term_require_all: Optional[bool] = None) -> Self:
        """The full-text query term, searches across all fields. By default,
        terms are joined with OR - to enforce that all terms in the term query
        must be in the noice to be a match, set term_require_all to True."""
        self.query = self.query.with_query(term, term_require_all)
        return self

    def with_title(self,
                   title: str,
                   title_require_all: Optional[bool] = None) -> Self:
        """Search in the title field. To require all words to match, set
        require_all to True."""
        self.query = self.query.with_title(title, title_require_all)
        return self

    def with_topic(self,
                   topic: Topic,
                   topic_require_all: Optional[bool] = None) -> Self:
        """Search in the topic field. To require all words to match, set
        require_all to True."""
        self.query = self.query.with_topic(topic, topic_require_all)
        return self

    def with_tags(self,
                  tags: str,
                  tags_require_all: Optional[bool] = None) -> Self:
        """Search in the tags field. To require all words to match, set
        require_all to True."""
        self.query = self.query.with_tags(tags, tags_require_all)
        return self

    def with_jurisdictions(
            self,
            jurisdictions: str,
            jurisdictions_require_all: Optional[bool] = None) -> Self:
        """Search in the jurisdictions field. To require all words to match, set
        require_all to True."""
        self.query = self.query.with_jurisdictions(jurisdictions,
                                                   jurisdictions_require_all)
        return self

    def with_sender(self,
                    sender: str,
                    sender_require_all: Optional[bool] = None) -> Self:
        """Search in the sender's name. Note - this is the person who filed
        the request, not necessairly the content owner! To require all words to
        match, set require_all to True."""
        self.query = self.query.with_sender(sender, sender_require_all)
        return self

    def with_principal(self,
                       principal: str,
                       principal_require_all: Optional[bool] = None) -> Self:
        """Search in the principal's name. Note - this is the organization
        that owns the content! I think. To require all words to match, set
        require_all to True."""
        self.query = self.query.with_principal(principal,
                                               principal_require_all)
        return self

    def with_recipient(self,
                       recipient: str,
                       recipient_require_all: Optional[bool] = None) -> Self:
        """Search in the receipient's name.  To require all words to match, set
        require_all to True."""
        self.query = self.query.with_recipient(recipient,
                                               recipient_require_all)
        return self

    def with_works_desc(self,
                        works_desc: str,
                        works_require_all: Optional[bool] = None) -> Self:
        """Search in the work's description.  To require all words to match, set
        require_all to True."""
        self.query = self.query.with_works_desc(works_desc, works_require_all)
        return self

    def with_action_taken(self, action_taken: str) -> Self:
        """Search based on the action taken on a notice."""
        self.query = self.query.with_action_taken(action_taken)
        return self

    def with_order(self, sort: Sort) -> Self:
        """Sorts the entries. (RelevancyDesc is the default option.)"""
        self.query = self.query.with_order(sort)
        return self

    def with_date_range(self, d1: date, d2: date) -> Self:
        """The date range. Asssumes you don't care about hours
        or seconds, just dates."""
        self.query = self.query.with_date_range(d1, d2)
        return self
