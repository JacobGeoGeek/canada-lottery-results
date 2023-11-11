from datetime import  datetime
from typing import Final
from bs4 import BeautifulSoup, ResultSet
from fastapi import HTTPException
import re
import math
from requests import Response, get

from src.common.entities.numbers_matched import NumbersMatched

from .entities.summary import Summary
from .entities.prize_breakdown import PrizeBreakdown

from .entities.result import Result
from .entities.classic import Classic
from .entities.guaranteed import Guaranteed
from .entities.gold_ball import GoldBall

_6_49_BASE_URL: Final[str] = "https://www.lottonumbers.com"
_6_49_PAGE: Final[str] = "/canada-6-49"

def fing_all_years() -> list[int]:
    """Return all lotto 6/49 years played"""
    return _get_6_49_years()

def find_649_results_by_year(year: int) -> list[Result]:
    """Return results by selected years"""
    url: str = f"{_6_49_BASE_URL}{_6_49_PAGE}-results-{year}"
    year_page: Response = get(url)

    if year_page.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Unable to fetch the year {year_page} results")
    
    html_content: BeautifulSoup = BeautifulSoup(year_page.text, "html.parser")
    table_results = html_content.find("table", class_="lotteryTable")

    trs = table_results.tbody.find_all("tr")
    results: Final[list[Result]] = []

    for tr in trs:
        url = tr.find("a")["href"]
        date: Final[date] = datetime.strptime(url.split("/")[-1], "%Y-%m-%d").date()
        classic: Final[Classic] = _get_classic_result(tr)

        detail_page: Response = get(f"{_6_49_BASE_URL}{url}")

        if detail_page.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Unable to fetch the Guarantted or Gold ball results for the date {date}")
        
        html_detail_content: BeautifulSoup = BeautifulSoup(detail_page.text, "html.parser")
        raffle_results: Final[ResultSet] = html_detail_content.find("div", id="lotto-raffle-results")
        table_breakdown: Final[ResultSet] = html_detail_content.find("table", class_="table-breakdown")
        
        guarantted: Final[Guaranteed] = _get_guaranteed_result(raffle_results, table_breakdown)
        gold_ball: Final[GoldBall] = _get_gold_ball_result(raffle_results, table_breakdown)

        results.append(Result(date=date, classic=classic, guaranteed=guarantted, goldBall=gold_ball))
    
    return results

def find_649_result_by_date(date: datetime.date) -> PrizeBreakdown:
    """Return the 6/49 result within a specific date"""
    date_result_page: Response = get(f"{_6_49_BASE_URL}{_6_49_PAGE}/results/{date.strftime('%Y-%m-%d')}")

    if date_result_page.status_code != 200:
        raise HTTPException(status_code=400, detail=f"The date {date} does not exist within the lotto 6/49 results")
    
    html_content: BeautifulSoup = BeautifulSoup(date_result_page.text, "html.parser")

    table_breakdown_result: Final[ResultSet] = html_content.find("table", class_="table-breakdown")

    if table_breakdown_result is None:
        raise HTTPException(status_code=400, detail=f"The prize breakdown results for the date {date} is not available.")

    tr_tags: Final[list[ResultSet]] = table_breakdown_result.tbody.find_all("tr")
    tr_tags.pop(-1) # Remove the last row representing the total
    
    return _process_prize_breakdown_results(tr_tags)

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

def _get_classic_result(tr: ResultSet) -> Classic:
    """Return the 6/49 classic result"""
    numbers: Final[list[int]] = list(map(lambda item: int(item.text), tr.find_all("li", class_="ball")))
    bonus: Final[int] = int(tr.find("li", class_="bonus-ball").text)

    td_tags = tr.find_all("td")
    prize: Final[float] = _format_prize_value(td_tags[-1].text) if len(td_tags) == 3 else None
    return Classic(numbers=numbers, bonus=bonus, prize=prize)

def _get_guaranteed_result(raffle_results: ResultSet, table_breakdown: ResultSet) -> Guaranteed | None:
    """Return the 6/49 guaranteed result"""
    title: Final[str] = "Guaranteed Prize Draw"
    h3_tags: Final[list[ResultSet]] = raffle_results.find_all("h3")
    
    h3: Final[list[ResultSet]] = list(filter(lambda h3: h3.text == title, h3_tags))

    if len(h3) != 1:
        return None

    if len(raffle_results.find_all("li")) != 2:
        return None
    
    draw_number: str = raffle_results.find_all("li")[-1].text

    if len(draw_number) == 0:
        return None

    tr_tags = table_breakdown.find_all("tr")
    last_row = tr_tags[-2]
    prize: Final[float] = _format_prize_value(last_row.find_all("td")[1].text)
    
    return Guaranteed(number=draw_number, prize=prize)


def _get_gold_ball_result(raffle_results: ResultSet, table_breakdown: ResultSet) -> GoldBall | None:
    """Return the 6/49 gold ball result"""
    title: Final[str] = "Gold Ball Number"
    h3_tags: Final[list[ResultSet]] = raffle_results.find_all("h3")

    h3: Final[list[ResultSet]] = list(filter(lambda h3: h3.text == title, h3_tags))

    if len(h3) != 1:
        return None
    
    if len(raffle_results.find_all("li")) != 2:
        return None
    
    draw_number: str = raffle_results.find_all("li")[-1].text

    if len(draw_number) == 0:
        return None

    tr_tags = table_breakdown.find_all("tr")
    last_row = tr_tags[-2]
    prize: Final[float] = _format_prize_value(last_row.find_all("td")[1].text)

    return GoldBall(number=draw_number, prize=prize, isGoldBallDrawn=(not math.isclose(prize, 1_000_000.00)))

def _process_prize_breakdown_results(tr_tags: list[ResultSet]) -> PrizeBreakdown:
    """Return the numbers matched"""
    free_play_ticket: Final[str] = "Free Play Ticket" 
    match_two: Final[str] = "Match 2"

    numbers_matched: Final[list[NumbersMatched]] = []

    total_winners: int = 0
    total_prize_fund: float = 0.0

    for tr in tr_tags:
        td_tags = tr.find_all("td")
        match: str = _format_match(td_tags[0].text)
        prize_per_winner: Final[float | str] = free_play_ticket if match == match_two else _format_prize_value(td_tags[1].text.strip())
        winners: Final[int] = _format_total_winners(td_tags[2].text)
        prize_fund: Final[float | None] = None if match == match_two else _format_prize_value(td_tags[3].text.strip())

        total_winners += winners

        if prize_fund is not None:
            total_prize_fund += prize_fund

        numbers_matched.append(NumbersMatched(match=match, prize_per_winner=prize_per_winner, total_winners=winners, prize_fund=prize_fund))
    
    return PrizeBreakdown(summary=Summary(total_winners=total_winners, total_prize_fund=total_prize_fund), numbers_matched=numbers_matched)


def _format_match(match: str) -> str:
    """Return the match"""
    return match.strip().replace("\n", "").replace("\r", "").replace("\t", "")

def _format_total_winners(total_winners: str) -> int:
    """Return the total winners"""
    return int(re.sub("[^\d]", "", total_winners.strip().replace(",", "")))

def _format_prize_value(prize: str) -> float | None:
    """Return the prize value"""
    prize = re.sub("[^\d\.]", "", prize.strip().replace(",", "").replace("\n", "").replace("\r", "").replace("\t", ""))

    if len(prize) == 0:
        return None

    return float(prize)

