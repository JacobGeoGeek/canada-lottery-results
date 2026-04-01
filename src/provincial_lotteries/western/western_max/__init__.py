

from typing import Final

from bs4 import BeautifulSoup
from requests import Response, get


_WESTERN_MAX_BASE_URL: Final[str] = "https://www.lottomaxnumbers.com"

def extract_all_years() -> list[int]:
    """Return all western max years played"""
    return _get_western_max_years()

def _get_western_max_years() -> list[int]:
    """Return all western max years played"""
    # Placeholder for the actual implementation
    year_past_page: Final[Response] = get(f"{_WESTERN_MAX_BASE_URL}/western-max/past-numbers")
    html_content = BeautifulSoup(year_past_page.content, "html.parser")
    return list(map(
        lambda a_tag: int(a_tag.text),
        html_content.find(class_="yearList").find_all("a")
    ))