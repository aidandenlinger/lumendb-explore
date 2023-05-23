from collections import Counter
from dataclasses import dataclass
from typing import Any, NamedTuple, Optional
from urllib.parse import urlparse

from lumen.SearchTypes import NoticeType, Topic


@dataclass(frozen=True)
class Notice:
    title: str
    type: NoticeType
    date_sent: str  # dateutil could be used to parse if that'd be useful
    date_received: str
    topics: list[Topic]
    tags: list[str]
    jurisdictions: list[str]
    infringing_urls: Counter[str]
    works: list[str]

    subject: Optional[str]
    body: Optional[str]
    language: Optional[str]
    action_taken: Optional[str]  # Yes, No, Partial, or blank

    # There are more fields, but this will get us started
    # https://github.com/berkmancenter/lumendatabase/wiki/Lumen-API-documentation#request


def notice_from_data(data: dict[str, Any]) -> Notice:
    return Notice(title=data['title'],
                  type=NoticeType(data['type'].lower()),
                  subject=data['subject'] if "subject" in data else None,
                  body=data['body'] if "body" in data else None,
                  date_sent=data['date_sent'],
                  language=data['language'],
                  date_received=data['date_received'],
                  topics=[Topic(topic) for topic in data['topics']],
                  tags=data['tags'],
                  jurisdictions=data['jurisdictions'],
                  action_taken=data['action_taken'],
                  infringing_urls=Counter([
                      url
                      for work in data['works']
                      for urlJSON in work['infringing_urls']
                      if (url := urlparse(urlJSON['url']).netloc)
                  ]),
                  works=[
                      work['description'].rstrip()
                      for work in data['works']
                  ])


class NameCount(NamedTuple):
    name: str
    instances: int


@dataclass(frozen=True)
class Metadata:
    # Content owners
    principals: list[NameCount]
    recipients: list[NameCount]
    # Those who actually filed the request
    senders: list[NameCount]
    topics: list[NameCount]
    tags: list[NameCount]
    countries: list[NameCount]
    lang: list[NameCount]
    action_taken: list[NameCount]

    # Those who submitted the request to Lumen, as far as I can tell
    submitters: list[NameCount]
    submitter_country: list[NameCount]

    # TODO
    # date: list[str]


def meta_from_facets(facets: dict[str, Any]) -> Metadata:

    def get_pair(name):
        return [
            NameCount(entry["key"], entry["doc_count"])
            for entry in facets[name]["buckets"] if entry["key"]
        ]

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


class SearchResult:
    notices: list[Notice]
    metadata: Metadata
    raw: dict[str, Any]

    def __init__(self, data: dict[str, Any]):
        self.notices = [notice_from_data(notice) for notice in data['notices']]
        self.metadata = meta_from_facets(data["meta"]["facets"])
        self.raw = data
