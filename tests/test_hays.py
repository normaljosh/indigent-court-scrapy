import pytest
from scrapy.http import HtmlResponse

from indigent.spiders.hays import HaysSpider


class TestCrawlHays:
    @pytest.mark.vcr()
    def test_get_filename_for_search_result(self, fake_page):
        spider = HaysSpider()
        file_name = spider.get_filename_for_search_result(fake_page)
        assert file_name == "hays-johnson-chris-2021-08-21.html"
