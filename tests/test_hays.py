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

    def test_remember_page_has_been_visited(self, fake_page):
        spider = HaysSpider()
        search_page = fake_page["search"]
        links = list(spider.get_links_from_search_page(search_page))
        assert len(links) == 2
        links_again = list(spider.get_links_from_search_page(search_page))
        assert len(links_again) == 0

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

    def test_dont_get_visited_page_again(self, fake_page):
        spider = HaysSpider()
        spider.explored_cases = {"19-4027CR-2"}
        search_page = fake_page["search"]
        links = list(spider.get_links_from_search_page(search_page))
        prefix = "http://public.co.hays.tx.us/CaseDetail.aspx?"
        assert len(links) == 1
        assert links[0].url == prefix + "CaseID=13029066"
        assert links[0].case_id == "17-4318CR-2"

    def test_get_earliest_case_event(self, fake_page):
        spider = HaysSpider()
        thc_page = fake_page["thc"]
        assert spider.get_earliest_event_date(thc_page) == dt.date(2011, 10, 12)

    def test_get_disposition_date(self, fake_page):
        spider = HaysSpider()
        thc_page = fake_page["thc"]
        assert spider.get_disposition_date(thc_page) == dt.date(2012, 8, 1)

    def test_get_counsel_status(self, fake_page):
        spider = HaysSpider()
        thc_page = fake_page["thc"]
        assert spider.get_counsel_status(thc_page) == "retained"

    def test_get_counsel_name(self, fake_page):
        spider = HaysSpider()
        thc_page = fake_page["thc"]
        assert spider.get_defense_counsel_name(thc_page) == "David Watts"

    def test_parse_case(self, fake_page):
        spider = HaysSpider()
        thc_page = fake_page["thc"]
        parsed = spider.parse(thc_page, case_id="19-4027CR-2")
        assert parsed.case_id == "19-4027CR-2"
        assert parsed.earliest_event == dt.date(2011, 10, 12)
        assert parsed.disposition_date == dt.date(2012, 8, 1)
        assert parsed.counsel_status == "retained"
        assert parsed.counsel_name == "David Watts"
        assert (
            parsed.charges[0].name
            == "POCS-TETRAHYDROCANNABINOL-ONE GRAM OR MORE BUT LESS THAN FOUR GRAMS"
        )
        assert parsed.charges[0].date == dt.date(2011, 10, 11)
        assert parsed.charges[0].statute == "481.116(c)"
        assert parsed.charges[0].level == "Third Degree Felony"
