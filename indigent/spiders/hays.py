import datetime as dt
import os
from urllib.parse import urlencode

import scrapy
from scrapy.http import FormRequest, Request, HtmlResponse


class HaysSpider(scrapy.Spider):
    name = "hays"
    main_page_url = "http://public.co.hays.tx.us/"
    calendar_page_url = "http://public.co.hays.tx.us/Search.aspx"

    judicial_officers = {
        "visiting_officer": "37809",
        "Boyer_Bruce": "39607",
        "Johnson_Chris": "48277",
        "Robison_Jack": "6140",
        "Sherri_Tibbe": "55054",
        "Henry_Bill": "25322",
        "Steel_Gary": "6142",
        "Updegrove_Robert": "38628",
        "Zelhart_Tacie": "48274",
    }

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
        return Request(url=url, callback=self.use_search_form,)

    def use_search_form(self, response):
        viewstate = response.css("#__VIEWSTATE").attrib["value"]

        today = dt.datetime.today()

        for daysago in range(1, 2):
            date_string = dt.datetime.strftime(
                today - dt.timedelta(days=daysago), format="%-m/%-d/%Y"
            )

            formdata = self.mk_cal_results_form_data(
                date_string, date_string, jo_id="48277", viewstate=viewstate
            )

            yield scrapy.FormRequest.from_response(
                response=response,
                formdata=formdata,
                callback=self.parse,
                cb_kwargs={"date_string": date_string},
            )

    def parse(self, response, date_string):
        """
        Just save the search result page as a file.

        To be replaced by a function that follows the links to the cases,
        with another callback function that parses the case pages.
        """
        if not os.path.exists("case_data"):
            os.mkdir("case_data")
        date_for_filename = dt.datetime.strptime(date_string, "%m/%d/%Y").strftime(
            "%Y-%m-%d"
        )
        file_name = f"{date_for_filename}.html"
        data_file_path = os.path.join("case_data", file_name)
        with open(data_file_path, "wb") as f:
            f.write(response.body)
        self.log(f"Saved file {file_name}")
