
from datetime import date, datetime
from typing import Final
from fastapi import HTTPException
from bs4 import BeautifulSoup, ResultSet
import requests

from .models.region import Region

from .entities.prize_breakdown import PrizeBreakdown
from .entities.location import Location
from .entities.winner import Winner
from .entities.numbers_matched import NumbersMatched
from .entities.summary import Summary
from .entities.numbers import Numbers

_LOTTOMAX_BASE_URL: Final[str] = "https://www.lottomaxnumbers.com"

def find_all_years() -> list[int]:
    """Return all lotto max years played"""
    return _get_lottomax_years()

def find_lotto_numbers_by_year(year: int) -> list[Numbers]:
    """Return result by selected years"""

    results: ResultSet = _get_table_result_by_year(year)

    return list(map(
        lambda row: Numbers(
            date=_format_date(row.a.text),
            prize=row.find(class_="jackpot").text[1:].replace(",", ""),
            numbers=_get_numbers(row.find_all(class_="ball")),
            bonus=row.find(class_="bonus-ball").text
        ),
        results
    ))

def find_lotto_result(date: datetime.date) -> PrizeBreakdown:
    """return the lottomax result within a specific date"""
    html_content = _get_result_page_by_date(date)

    div_summary: Final[list[ResultSet]] = [
        div.find(class_="contentBox")
        for div in html_content.find(class_="prizeStatsBox").find_all(class_="box")
    ]

    table_content: Final[list[ResultSet]] = html_content.find(
        class_="lottoMaxBox").tbody.find_all("tr")

    numbers_matched: Final[list[NumbersMatched]] = _get_numbers_matched(table_content)

    total_prize_fund: Final[float] = _get_total_prize_fund(numbers_matched)

    summary: Final[Summary] = _get_stats_summary(div_summary, total_prize_fund)

    return PrizeBreakdown(summary=summary, numbers_matched=numbers_matched)


def find_lotto_result_by_date_and_region(
    date: datetime.date,
    region: Region) -> list[NumbersMatched]:
    """Return the lotto result from specific date and region"""

    region_class: Final[str] = _get_class_by_region(region)
    html_content = _get_result_page_by_date(date)

    table_content: Final[list[ResultSet]] = html_content.find(
        class_=region_class).tbody.find_all("tr")

    return _get_numbers_matched(table_content)

def _get_result_page_by_date(date: datetime.date) -> ResultSet:
    """Return the result website within a specific date"""
    year: Final[int] = date.year

    results: ResultSet = _get_table_result_by_year(year)

    date_results: Final[list[date]] = list(map(
        lambda row: _format_date(row.a.text),
        results
        ))

    if date not in date_results:
        raise HTTPException(
            400,
            f"The date {date} does not exist within the lotto max past result"
        )

    result_page: requests.Response = requests.get(
        f"{_LOTTOMAX_BASE_URL}/numbers/lotto-max-result-{date.strftime('%m-%d-%Y')}"
        ).text

    return BeautifulSoup(result_page, "html.parser")

def _get_class_by_region(region: Region) -> str:
    if region not in Region:
        raise HTTPException(
            400,
            f"The region {region} is invalid"
        )

    if region is Region.ATLANTIC:
        return "atlanticBox"

    if region is Region.BRITISH_COLUMBIA:
        return "bcBox"

    if region is Region.ONTARIO:
        return "ontarioBox"

    if region is Region.QUEBEC:
        return "quebecBox"

    if region is Region.WESTERN_CANADA:
        return "westernBox"

def _get_total_prize_fund(numbers_matched: list[NumbersMatched]) -> float:
    numbers_with_prize_fund: Final[list[NumbersMatched]] = list(
        filter(
            lambda number_matched: number_matched.prize_fund is not None,
            numbers_matched
            ))

    return round(sum(map(lambda x: x.prize_fund, numbers_with_prize_fund)), 2)

def _get_numbers_matched(numbers_matched_table: list[ResultSet]) -> list[NumbersMatched]:
    results: Final[list[NumbersMatched]] = []

    if not numbers_matched_table:
        return results

    numbers_matched_table.pop()

    tds: Final[list[ResultSet]] = list(map(lambda tr: tr.find_all("td"), numbers_matched_table))

    for td_content in tds:
        match: Final[str] = td_content[0].strong.text
        prize_per_winner: Final[str] = td_content[1].text.strip().replace(",", "").replace("$", "")

        total_winners: Final[int] = _get_number_winners(td_content[2])
        prize_fund: str or None = td_content[3].text.strip()

        if prize_fund == "-":
            prize_fund = None
        else:
            prize_fund = prize_fund.replace(",", "")[1:]

        number_matched: Final[NumbersMatched] = NumbersMatched(match=match, prize_per_winner=prize_per_winner, total_winners=total_winners, prize_fund=prize_fund)

        results.append(number_matched)

    return results

def _get_number_winners(td_content: ResultSet) -> int:
    total: int = 0
    location: list[Location] = []

    if len(td_content.find_all(class_="regionWinners")) != 0:
        region_winner: list[str] = list(map(
            lambda div: div.find(class_="region").text,
            td_content.find_all(class_="regionWinners")
            ))

        location.extend(list(map(
            lambda region: _get_winner_location(region.split(": ")),
            region_winner
            )))

        total = sum(map(lambda location: location.total, location))
    elif td_content.find("span") is not None:
        total = int(td_content.text.strip().replace(" ", "").split("-")[1])
    else:
        total= int(td_content.text.strip().replace(",", ""))

    return total

def _get_winner_location(region: list[str]) -> Location:
    return Location(region=region[0], total=region[1].replace(",", ""))

def _get_stats_summary(summary_contents: list[ResultSet], total_prize_fund: float) -> Summary:
    stat_class: str = "stat"

    ticket_sold: str = summary_contents[0].find(class_=stat_class).text.replace(",", "")

    if not ticket_sold:
        ticket_sold = None

    total_sales: str = summary_contents[0].find(class_="statSmall").text
    total_sales = total_sales.split(": ")[1].replace(",", "")[1:]

    if not total_sales:
        total_sales = None

    total_winners: str = summary_contents[1].find(class_=stat_class).text.replace(",", "")
    winning_ratio: str  = summary_contents[2].find(class_=stat_class).text

    sales_difference: str = summary_contents[3].find(class_=stat_class).text

    return Summary(
        ticket_sold=ticket_sold,
        total_sales=total_sales,
        total_winners=total_winners,
        total_prize_fund=total_prize_fund,
        winning_ratio=(int(winning_ratio.split(" ")[0]) / 100),
        sales_difference_previous_draw=sales_difference
    )

def _get_table_result_by_year(year: int) -> ResultSet:
    year_page: requests.Response = requests.get(f"{_LOTTOMAX_BASE_URL}/numbers/{year}").text
    html_content = BeautifulSoup(year_page, "html.parser")

    result_rows: ResultSet = html_content.find_all("tr")

    for i, row in enumerate(result_rows):
        if not row.find("ul", class_="balls"):
            result_rows.pop(i)

    return result_rows


def _get_lottomax_years() -> list[int]:
    """Return all lotto max years"""
    year_past_page: requests.Response = requests.get(
        f"{_LOTTOMAX_BASE_URL}/past-numbers").text
    html_content = BeautifulSoup(year_past_page, "html.parser")

    return list(map(
        lambda a_tag: int(a_tag.text),
        html_content.find(class_="yearList").find_all("a")
    ))


def _format_date(date_value: str) -> date:
    """Map the date to MM-DD-YYYY"""
    return datetime.strptime(date_value, "%B %d %Y").date()


def _get_numbers(li_tags) -> list[int]:
    """Extract the number results with the li tags"""
    return list(map(lambda li: int(li.text), li_tags))
