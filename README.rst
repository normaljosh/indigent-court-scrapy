indigent-court-scrapy
=====================

A scraping experiment for an Open Austin data project about appointed counsel in Texas courts.

.. image:: https://coveralls.io/repos/github/open-austin/indigent-court-scrapy/badge.svg?branch=main
    :target: https://coveralls.io/github/open-austin/indigent-court-scrapy?branch=main
    :alt: Coveralls Code Coverage

.. image:: https://github.com/open-austin/indigent-court-scrapy/actions/workflows/python-package.yml/badge.svg
    :target: https://github.com/open-austin/indigent-court-scrapy/actions
    :alt: GitHub Actions Workflow

The goal of the project is to support research by
the `Texas Indigent Defense Commission <tidc.texas.gov>`_ about the caseloads and effectiveness of appointed
defense attorneys.

See the #p-indigent-defense-stats channel on https://open-austin.slack.com/ to learn more
about the project.

To scrape, install the `scrapy` package and run:

    scrapy crawl hays

See the `Scrapy docs <http://doc.scrapy.org/en/latest/topics/tutorial.html>`_ for more information.

Open Austin members have created multiple repositories with different strategies for scraping this
website. In addition to this latest version based on `scrapy`,
`our inactive first prototype <https://github.com/open-austin/indigent-defense-scraper>`_ was based on
`spatula <https://github.com/jamesturk/spatula>`_, our `second scraper <https://github.com/derac/hays-scraper>`_
is based directly on `requests <http://docs.python-requests.org/en/latest/>`_, and we also explored
using `the biglocalnews court-scraper project <https://github.com/biglocalnews/court-scraper>`_.