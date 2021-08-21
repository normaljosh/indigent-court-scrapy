import datetime as dt

import pytest
from scrapy.http import HtmlResponse

from indigent.spiders.hays import HaysSpider


class TestCrawlHays:
    def test_get_filename_for_search_result(self):
        spider = HaysSpider()
        file_name = spider.get_filename_for_search_result(start_date=dt.date(2021, 8, 21), jo_id="48277")
        assert file_name == "48277-2021-08-21.html"
