import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Counter, Dict, List, NamedTuple, Optional
from urllib.parse import urlparse

from lumen.SearchTypes import NoticeType, Topic


@dataclass(frozen=True)
class Notice:
    title: str
    type: NoticeType
    sender_name: str
    recipient_name: str
    principal_name: Optional[str]
    date_sent: str  # dateutil could be used to parse if that'd be useful
    date_received: str
    topics: List[Topic]
    tags: List[str]
    jurisdictions: List[str]
    infringing_urls: Counter[str]
    works: List[str]

    subject: Optional[str]
    body: Optional[str]
    language: Optional[str]
    action_taken: Optional[str]  # Yes, No, Partial, or blank

    # There are more fields, but this will get us started
    # https://github.com/berkmancenter/lumendatabase/wiki/Lumen-API-documentation#request


def notice_from_data(data: Dict[str, Any]) -> Notice:
    return Notice(
        title=data['title'],
        type=NoticeType(data['type'].lower()),
        sender_name=data['sender_name'],
        recipient_name=data['recipient_name'],
        principal_name=data['principal_name']
        if "principal_name" in data else None,
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
            url for work in data.get('works', [])
            for urlJSON in work.get('infringing_urls', [])
            if (url := urlparse(urlJSON['url']).netloc)
        ]),
        works=[
            work['description'].rstrip() for work in data.get('works', [])
            if 'description' in work and work['description'] is not None
        ])


class NameCount(NamedTuple):
    name: str
    instances: int


@dataclass(frozen=True)
class Metadata:
    # Content owners
    principals: List[NameCount]
    recipients: List[NameCount]
    # Those who actually filed the request
    senders: List[NameCount]
    topics: List[NameCount]
    tags: List[NameCount]
    countries: List[NameCount]
    lang: List[NameCount]
    action_taken: List[NameCount]

    # Those who submitted the request to Lumen, as far as I can tell
    submitters: List[NameCount]
    submitter_country: List[NameCount]

    # TODO
    # date: list[str]


def meta_from_facets(facets: Dict[str, Any]) -> Metadata:

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
    notices: List[Notice]
    metadata: Metadata
    raw: Dict[str, Any]

    def __init__(self, data: Dict[str, Any]):
        self.notices = [notice_from_data(notice) for notice in data['notices']]
        self.metadata = meta_from_facets(data["meta"]["facets"])
        self.raw = data


def load_all_cache_entries(cache: Path) -> List[Notice]:
    """Loads all .json files from a cache and collects all of their entries
    into a list."""
    entries: List[Notice] = []

    for file in cache.iterdir():
        if file.suffix == ".json":
            with file.open() as input:
                data = json.load(input)
                entries.extend(
                    notice_from_data(notice)
                    for notice in data.get('notices', []))

    return entries
