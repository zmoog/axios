from dataclasses import dataclass
from typing import Any

import requests
from lxml import html

from .models import Credentials, Grade, Profile

START_URL = "https://family.axioscloud.it/Secret/REStart.aspx?Customer_ID="
FAMILY_URL = "https://family.axioscloud.it/Secret/REFamily.aspx"


@dataclass
class State:
    """State in an ASP.NET web application."""

    viewstate: str = ""
    viewstategenerator: str = ""
    eventvalidation: str = ""

    @classmethod
    def fromtree(cls, tree: html.HtmlElement):
        return cls(
            viewstate=tree.xpath('//input[@id="__VIEWSTATE"]/@value'),
            viewstategenerator=tree.xpath(
                '//input[@id="__VIEWSTATEGENERATOR"]/@value'
            ),
            eventvalidation=tree.xpath(
                '//input[@id="__EVENTVALIDATION"]/@value'
            ),
        )


class Navigator:
    def __init__(
        self,
        credentials: Credentials,
        session: requests.Session = requests.Session(),
    ):
        self.credentials = credentials
        self.session = session
        self.state = State()

    def login(self) -> Profile:
        """Login to the Axios Family web application."""

        startUrl = START_URL + self.credentials.customer_id

        # Get the login page
        resp = self.session.get(startUrl)
        dump_to_file("login.1.html", resp.text)

        self.state = State.fromtree(html.fromstring(resp.text))

        start_payload = {
            "__VIEWSTATE": self.state.viewstate,
            "__VIEWSTATEGENERATOR": self.state.viewstategenerator,
            "__EVENTVALIDATION": self.state.eventvalidation,
            "ibtnRE.x": 0,
            "ibtnRE.y": 0,
            "mha": "",
        }

        # I don't know why we need to do this is, but it's required
        resp = self.session.post(
            startUrl, data=start_payload, headers=headers_for(startUrl)
        )
        dump_to_file("login.2.html", resp.text)
        tree = html.fromstring(resp.text)
        self.state = State.fromtree(tree)

        login_payload = {
            "__LASTFOCUS": "",
            "__EVENTTARGET": "",
            "__VIEWSTATE": self.state.viewstate,
            "__VIEWSTATEGENERATOR": self.state.viewstategenerator,
            "__EVENTVALIDATION": self.state.eventvalidation,
            "txtImproveDone": "",
            "txtUser": self.credentials.username,
            "txtPassword": self.credentials.password,
            "btnLogin": "Accedi",
        }

        # does the actual login
        resp = self.session.post(
            "https://family.axioscloud.it/Secret/RELogin.aspx",
            data=login_payload,
            headers=headers_for(startUrl),
        )

        dump_to_file("login.3.html", resp.text)

        tree = html.fromstring(resp.text)
        self.state = State.fromtree(tree)

        # look for the user name in the page, if it's not there,
        # we're not logged in
        name = tree.xpath('//span[@id="lblUserName"]')
        if not name:
            raise Exception("Login failed")

        customer_title = tree.xpath('//span[@id="lblCustomerTitle"]')
        customer_name = tree.xpath('//span[@id="lblCustomerName"]')

        return Profile(
            self.credentials.customer_id,
            name[0].text,
            customer_title[0].text,
            customer_name[0].text,
        )

    def list_grades(self):
        """List the grades for the logged in user."""

        payload = {
            "__LASTFOCUS": "",
            "__EVENTTARGET": "FAMILY",
            "__EVENTARGUMENT": "RED",
            "__VIEWSTATE": self.state.viewstate,
            "__VIEWSTATEGENERATOR": self.state.viewstategenerator,
            "__EVENTVALIDATION": self.state.eventvalidation,
            "ctl00$ContentPlaceHolderMenu$ddlAnno": "2022",
            "ctl00$ContentPlaceHolderMenu$ddlFT": "FT01",
            "ctl00$ContentPlaceHolderBody$txtDataSelezionataCAL": "13/11/2022",  # FIXME: replace with today's date
            "ctl00$ContentPlaceHolderBody$txtFunctionSelected": "nothing",
            "ctl00$ContentPlaceHolderBody$txtAluSelected": "00002401",  # ????
            "ctl00$ContentPlaceHolderBody$txtIDAluSelected": "0",
        }

        resp = self.session.post(
            FAMILY_URL,
            data=payload,
            headers=headers_for(FAMILY_URL),
        )
        dump_to_file("family.1.html", resp.text)

        tree = html.fromstring(resp.text)
        self.state = State.fromtree(tree)

        rows = tree.xpath('//div[@id="votiEle"]/div/table/tbody/tr')
        grades = []
        for row in rows:
            grades.append(
                Grade(
                    date=first(row.xpath("td[1]/text()")),
                    subject=first(row.xpath("td[2]/text()")),
                    kind=first(row.xpath("td[3]/text()")),
                    value=first(row.xpath("td[4]/span/text()")),
                    target=first(row.xpath("td[5]/text()")),
                    comment=first(row.xpath("td[6]/text()")),
                    teacher=first(row.xpath("td[7]/text()")),
                )
            )

        return grades


def first(sequence, defaultValue: Any = ""):
    return sequence[0] if sequence else defaultValue


def headers_for(url: str) -> dict:
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://family.axioscloud.it",
        "Referer": url,
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    }


def dump_to_file(filename, data):
    with open(f"/tmp/{filename}", "w") as f:
        f.write(data)
