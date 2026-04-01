
from datetime import datetime
from typing import Final

from bs4 import BeautifulSoup, ResultSet
from requests import Response, get

_WESTERN_MAX_BASE_URL: Final[str] = "https://www.wclc.com"

def fetch_western_max_result(date: datetime.date) -> Response:
    """Fetch the Western Max result for a specific date"""
    pass
    

def extract_all_years() -> list[int]:
    """Return all years from the external data"""
    pass

# TODO return the correct type
def extract_lotto_numbers_by_year(year: int) -> list[dict]:
    """Return result by selected years"""
    html_content = _get_result_page_by_date(datetime.date)

    winners_numbers: Final[list[int]] = _extract_winnning_number(html_content)
    bonus_number: Final[int] = _extract_bonus_number(html_content)

    breakdowns: Final[ResultSet] = html_content.find_all(class_="prizeBreakdownTable")
    main_breakdown: Final[ResultSet] = breakdowns[0]
    one_millions_breakdown: Final[ResultSet] = breakdowns[1]
    extra_breakdown: Final[ResultSet] = breakdowns[2]

    

def extract_lotto_result(date: datetime.date) -> dict:
    """Return the lottomax result within a specific date"""
    pass

def _get_result_page_by_date(date: datetime.date) -> ResultSet:
    """Fetch the result page HTML content for a specific date"""
    result: Response = get(f"{_WESTERN_MAX_BASE_URL}/winning-numbers/western-max-extra.htm")

    if result.status_code != 200:
        raise Exception("Failed to fetch data from Western Max external source")

    html_content: ResultSet = BeautifulSoup(result.text, "html.parser")

    past_winning_numbers: ResultSet = html_content.findAll(class_="pastWinNum")
    winning_number_for_date: ResultSet = next(
        (item for item in past_winning_numbers if datetime.strptime(item.find(class_="pastWinNumDate").find("h4").text.strip(), "%A, %B %d, %Y").date() == date),
        None
    )

    if not winning_number_for_date:
        raise Exception(f"No results found for the date {date}")
    
    draw_number_url: Final[str] = winning_number_for_date.find(class_="pastWinNumPrizeBreakdown").get("rel")

    draw_result_page: Response = get(f"{_WESTERN_MAX_BASE_URL}{draw_number_url}")

    if draw_result_page.status_code != 200:
        raise Exception(f"Failed to fetch draw result page for the date {date} from Western Max external source")

    return BeautifulSoup(draw_result_page.text, "html.parser")

def _extract_winnning_number(html_content: ResultSet) -> list[int]:
    """Extract winning numbers from the HTML content"""
    winning_numbers_section: ResultSet = html_content.findAll(class_="pastWinNumber")
    return list(map(lambda number_tag: int(number_tag.text.strip()), winning_numbers_section))

def _extract_bonus_number(html_content: ResultSet) -> int:
    """Extract bonus number from the HTML content"""
    bonus_number_section: ResultSet = html_content.find(class_="pastWinNumberBonus")
    return int(bonus_number_section.text.strip().replace("Bonus ", ""))

  