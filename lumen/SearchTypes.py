import sys
from enum import auto

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from strenum import StrEnum


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


class NoticeType(StrEnum):
    Counternotice = auto()
    CourtOrder = auto()
    DataProtection = auto()
    Defamation = auto()
    Dmca = "DMCA"
    LawEnforcementRequest = auto()
    Other = auto()
    PrivateInformation = auto()
    GovernmentRequest = auto()
    Trademark = auto()
