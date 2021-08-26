# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
import datetime as dt
from typing import List


import scrapy


@dataclass
class CaseIDWithURL:
    """
    This class is used to store the case ID and the URL.
    """

    case_id: str
    url: str


@dataclass
class ChargeItem:
    name: str
    date: dt.date
    statute: str
    level: str


@dataclass
class CaseItem:
    case_id: str
    earliest_event: dt.date
    disposition_date: dt.date
    counsel_status: str
    counsel_name: str
    charges: List[ChargeItem]
