import os

import pytest
from scrapy.http import Request, HtmlResponse


def fake_response_from_file(file_name, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    if not url:
        url = 'http://www.example.com'

    request = Request(url=url)
    if not file_name[0] == '/':
        responses_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(responses_dir, file_name)
    else:
        file_path = file_name
    file_content = open(file_path, 'r').read()

    response = HtmlResponse(url=url,
        request=request,
        body=file_content, encoding='utf-8')
    return response

@pytest.fixture(scope="class")
def fake_page():
    return {
        "search": fake_response_from_file(
            file_name="pages/hays-johnson-chris-2021-08-21.html",
            url="https://public.co.hays.tx.us/Search.aspx?ID=900&NodeID=100%2c101%2c102%2c103%2c200%2c201%2c202%2c203%2c204%2c6112%2c400%2c401%2c402%2c403%2c404%2c405%2c406%2c407%2c6111%2c6114&NodeDesc=All+Courts"
            )}
