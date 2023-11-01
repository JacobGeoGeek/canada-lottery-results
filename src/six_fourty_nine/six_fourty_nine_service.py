

from datetime import datetime
from typing import Final
from bs4 import BeautifulSoup
from fastapi import HTTPException

from requests import Response, get


_6_49_BASE_URL: Final[str] = "https://www.lottonumbers.com"
_6_49_PAGE: Final[str] = "/canada-6-49"


def fing_all_years() -> list[int]:
    """Return all lotto 6/49 years played"""
    return _get_6_49_years()


def _get_6_49_years() -> list[int]:
    """Return all lotto 6/49 years played"""

    six_foyrty_nine_page: Response = get(f"{_6_49_BASE_URL}{_6_49_PAGE}")
    html_content: BeautifulSoup = BeautifulSoup(six_foyrty_nine_page.text, "html.parser")

    left_menu_div = html_content.find('div', {'id': 'leftMenu'}).find_all("div", class_="sidebar-container")
    archived_container = list(filter(lambda div: div.find("div", class_="sideTitle").text == "Archived Numbers", left_menu_div))

    if len(archived_container) != 1:
        raise HTTPException(status_code=500, detail="Unable to fetch the years results")
    
    archived_container = archived_container[0]
    years_urls = archived_container.find_all("li", class_=["lottery", "archiveMore"])

    years: Final[list[int]] = []

    for year_url in years_urls:
        year_text: str = year_url.find("a").text

        if len(year_text.split(" ")) == 2:
            year: int = int(year_text.split(" ")[0])
            years.append(year)

    return years
