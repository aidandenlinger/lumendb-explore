from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Optional, Self
from urllib.parse import quote_plus

from lumen.LumenAPIManager import LumenAPIManager


class Topic(StrEnum):
    Trademark = "Trademark",
    JohnDoe = "John Doe Anonymity",
    Defamation = "Defamation",
    Response = "Responses",
    Derivative = "Derivative Works",
    FanFiction = "Fan Fiction",
    Domain = "Domain Names and Trademarks",
    TradeSecret = "Trade Secret",
    NoAction = "No Action",
    DMCASubpoena = "DMCA Subpoenas",
    Publicity = "Right of Publicity",
    CourtOrder = "Court Orders",
    ECommercePatent = "E-Commerce Patents",
    Udrp = "UDRP",
    Acpa = "ACPA",
    Piracy = "Piracy or Copyright Infringement",
    DocumentingDomain = "Documenting Your Domain Defense",
    DMCANotice = "DMCA Notices",
    DMCACircumvention = "Anticircumvention (DMCA)",
    Copyright = "Copyright",
    FairUse = "Copyright and Fair Use",
    RevEngineering = "Reverse Engineering",
    Criticism = "Protest, Parody and Criticism Sites",
    Linking = "Linking",
    LawEnforce = "Law Enforcement Requests",
    Patent = "Patent",
    International = "International",
    # "правото да бъдеш забравен",
    # "Recht Om Vergeten Te Worden",
    # "O Pravu Osobe Da Bude Zaboravljena?",
    # " El Derecho Al Olvido",
    # "\"Recht auf Vergessen\" ",
    EUPrivacy = "EU - Right to Be Forgotten",
    DMCASafeHarbor = "DMCA Safe Harbor",
    GovRequest = "Government Requests",
    # "Lumen",
    Counterfeit = "Counterfeit"


@dataclass(frozen=True)
class Metadata:
    # Content owners
    principals: list[tuple[str, int]]
    recipients: list[tuple[str, int]]
    # Those who actually filed the request
    senders: list[tuple[str, int]]
    topics: list[tuple[str, int]]
    tags: list[tuple[str, int]]
    countries: list[tuple[str, int]]
    lang: list[tuple[str, int]]
    action_taken: list[tuple[str, int]]

    # Those who submitted the request to Lumen, as far as I can tell
    submitters: list[tuple[str, int]]
    submitter_country: list[tuple[str, int]]

    # date: list[str]


def meta_from_facets(facets: dict[str, Any]) -> Metadata:

    def get_pair(name):
        return [(entry["key"], entry["doc_count"])
                for entry in facets[name]["buckets"] if entry["key"] != ""]

    return Metadata(senders=get_pair("sender_name_facet"),
                    recipients=get_pair("recipient_name_facet"),
                    principals=get_pair("principal_name_facet"),
                    submitters=get_pair("submitter_name_facet"),
                    topics=get_pair("topic_facet"),
                    tags=get_pair("tag_list_facet"),
                    countries=get_pair("country_code_facet"),
                    submitter_country=get_pair("submitter_country_code_facet"),
                    lang=get_pair("language_facet"),
                    action_taken=get_pair("action_taken_facet"))


@dataclass(frozen=True)
class SearchData:
    metadata: Metadata
    raw: dict[str, Any]


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
            "term": quote_plus(term),
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
            "title": quote_plus(title),
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
            "topics": quote_plus(topic),
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
            "tags": quote_plus(tags),
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
            "jurisdictions": quote_plus(jurisdictions),
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
            "sender_name": quote_plus(sender),
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
            "principal_name": quote_plus(principal),
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
            "recipient_name": quote_plus(recipient),
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
            "works": quote_plus(works_desc),
        })

        if works_require_all:
            self.params.update(
                {"works-require-all": str(works_require_all).lower()})

        return self

    def with_action_taken(self, action_taken: str) -> Self:
        """Search based on the action taken on a notice."""
        self.params.update({"action_taken": quote_plus(action_taken)})

        return self

    def with_amount(self, num_of_entries: int) -> Self:
        """Set the amount of results you will get. Cannot go past 10000."""
        if num_of_entries > 10000:
            # Todo: We can paginate (request a page of 10000 entries, then
            # the next page of 10000 entries, etc)
            raise Exception("Requested too many entries!")
        self.params.update({"per_page": str(num_of_entries)})
        return self

    # TODO: facet country code, date, language

    def search(self) -> SearchData:
        if len(self.params) == 0:
            raise Exception("No search parameters!")
        data = self.manager._req("/notices/search.json", self.params)
        return SearchData(metadata=meta_from_facets(data["meta"]["facets"]),
                          raw=data)
