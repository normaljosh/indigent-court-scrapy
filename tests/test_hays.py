import datetime as dt

import pytest
from scrapy.http import HtmlResponse

from indigent.spiders.hays import HaysSpider


class TestCrawlHays:
    def test_get_filename_for_search_result(self):
        spider = HaysSpider()
        file_name = spider.get_filename_for_search_result(
            start_date=dt.date(2021, 8, 21), jo_id="48277"
        )
        assert file_name == "48277-2021-08-21.html"

    def test_get_links_from_search_page(self, fake_page):
        spider = HaysSpider()
        search_page = fake_page["search"]
        links = list(spider.get_links_from_search_page(search_page))
        prefix = "http://public.co.hays.tx.us/CaseDetail.aspx?"
        assert len(links) == 2
        assert links[0].url == prefix + "CaseID=13114245"
        assert links[0].case_id == "19-4027CR-2"
        assert links[1].url == prefix + "CaseID=13029066"
        assert links[1].case_id == "17-4318CR-2"
