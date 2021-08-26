# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

import scrapy


@dataclass
class CaseIDWithURL:
    """
    This class is used to store the case ID and the URL.
    """

    case_id: str
    url: str


@dataclass
class IndigentItem:
    pass
