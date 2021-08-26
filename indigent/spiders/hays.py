import datetime as dt
import os
from typing import Iterator, Optional, Set
from urllib.parse import urlencode

import scrapy
from scrapy.http import FormRequest, Request, HtmlResponse

from indigent.items import CaseIDWithURL, CaseItem, ChargeItem


class HaysSpider(scrapy.Spider):
    name = "hays"
    main_page_url = "http://public.co.hays.tx.us/"
    calendar_page_url = "http://public.co.hays.tx.us/Search.aspx"

    judicial_officers = {
        "visiting officer": "37809",
        "Boyer, Bruce": "39607",
        "Johnson, Chris": "48277",
        "Robison, Jack": "6140",
        "Sherri, Tibbe": "55054",
        "Henry, Bill": "25322",
        "Steel, Gary": "6142",
        "Updegrove, Robert": "38628",
        "Zelhart, Tacie": "48274",
    }

    def __init__(self, category=None, *args, **kwargs):
        super(HaysSpider, self).__init__(*args, **kwargs)
        self.explored_cases: Set[str] = set()

    @classmethod
    def mk_cal_results_form_data(
        cls, startDate: str, endDate: str, jo_id, viewstate: str
    ):
        return {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": "BBBC20B8",
            "__EVENTVALIDATION": "/wEWAgKEib6eCQKYxoa5CABRE1bdUnTyMmdE4n0IKj4cWw4t",
            "SearchBy": "3",
            "ExactName": "on",
            "CaseSearchMode": "CaseNumber",
            "CaseSearchValue": "",
            "CitationSearchValue": "",
            "CourtCaseSearchValue": "",
            "PartySearchMode": "Name",
            "AttorneySearchMode": "Name",
            "LastName": "",
            "FirstName": "",
            "cboState": "AA",
            "MiddleName": "",
            "DateOfBirth": "",
            "DriverLicNum": "",
            "CaseStatusType": "0",
            "DateFiledOnAfter": "",
            "DateFiledOnBefore": "",
            "cboJudOffc": jo_id,
            "chkCriminal": "on",
            "chkDtRangeCriminal": "on",
            "chkDtRangeFamily": "on",
            "chkDtRangeCivil": "on",
            "chkDtRangeProbate": "on",
            "chkCriminalMagist": "on",
            "chkFamilyMagist": "on",
            "chkCivilMagist": "on",
            "chkProbateMagist": "on",
            "DateSettingOnAfter": startDate,
            "DateSettingOnBefore": endDate,
            "SortBy": "fileddate",
            "SearchSubmit": "Search",
            "SearchType": "JUDOFFC",
            "SearchMode": "JUDOFFC",
            "NameTypeKy": "",
            "BaseConnKy": "",
            "StatusType": "true",
            "ShowInactive": "",
            "AllStatusTypes": "true",
            "CaseCategories": "CR",
            "RequireFirstName": "True",
            "CaseTypeIDs": "",
            "HearingTypeIDs": "",
        }

    def start_requests(self):
        return [
            scrapy.FormRequest(url=self.main_page_url, callback=self.go_to_calendar)
        ]

    def go_to_calendar(self, response):
        calendar_query = {
            "ID": "900",
            "NodeID": "100,101,102,103,200,201,202,203,204,6112,400,401,402,403,404,405,406,407,6111,6114",
            "NodeDesc": "All%20Courts",
        }
        url = f"{self.calendar_page_url}?{urlencode(calendar_query)}"
        return Request(
            url=url,
            callback=self.use_search_form,
        )

    def use_search_form(self, response):
        viewstate = response.css("#__VIEWSTATE").attrib["value"]

        end_date = dt.datetime.today()
        start_date = dt.datetime(2021, 10, 26)
        jo_id = "39607"

        start_string = start_date.strftime("%-m/%-d/%Y")
        end_string = end_date.strftime("%-m/%-d/%Y")

        formdata = self.mk_cal_results_form_data(
            start_string, start_string, jo_id=jo_id, viewstate=viewstate
        )

        yield scrapy.FormRequest.from_response(
            response=response,
            formdata=formdata,
            callback=self.parse_search_results,
            cb_kwargs={"start_date": start_date, "jo_id": jo_id},
        )

    def get_filename_for_search_result(self, start_date: dt.date, jo_id: str):
        """Get filename where search result HTML page can be saved."""
        return f"{jo_id}-{start_date.strftime('%Y-%m-%d')}.html"

    def get_links_from_search_page(self, response) -> Iterator[CaseIDWithURL]:
        for link in response.css("a[href*=CaseDetail]"):
            if link:
                case_id = link.css("::text").get()
                if case_id not in self.explored_cases:
                    self.explored_cases.add(case_id)
                    yield CaseIDWithURL(
                        case_id=case_id,
                        url=self.main_page_url + link.attrib["href"],
                    )

    def parse_search_results(self, response, start_date: dt.date, jo_id: str):
        """
        Just save the search result page as a file.

        To be replaced by a function that follows the links to the cases,
        with another callback function that parses the case pages.
        """

        file_name = self.get_filename_for_search_result(start_date, jo_id)
        data_file_path = os.path.join("search_results", self.name, file_name)
        with open(data_file_path, "wb") as f:
            f.write(response.body)
        self.log(f"Saved file {file_name}")

        for case in self.get_links_from_search_page(response):
            yield Request(
                url=case.url, callback=self.parse, cb_kwargs={"case_id": case.case_id}
            )

    def get_earliest_event(self, response) -> Optional[dt.datetime]:
        """
        Get the earliest date from the OTHER EVENTS AND HEARINGS table.
        """
        for row in response.css("table.CaseHistory tr"):
            if row.css("td.CaseHistoryDate"):
                date_string = row.css("td.CaseHistoryDate::text").get()
                date = dt.datetime.strptime(date_string, "%m/%d/%Y")
                return date
        return None

    def parse(self, response, case_id: str):
        data_file_path = os.path.join("register_pages", self.name, f"{case_id}.html")
        with open(data_file_path, "wb") as f:
            f.write(response.body)
        self.log(f"Saved file {case_id}.html")

        earliest_event = self.get_earliest_event(response)
        return CaseItem(case_id=case_id, earliest_event=earliest_event)
