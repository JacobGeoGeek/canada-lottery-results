from datetime import  datetime
from io import BytesIO
from typing import Final
from zipfile import ZipFile
from bs4 import BeautifulSoup, ResultSet
import re
from pandas import DataFrame, read_csv, to_datetime
from requests import Response, get

from src.common.models.numbers_matched import NumbersMatched
from src.common.models.summary import Summary

from .models.prize_breakdown import PrizeBreakdown

from .models.result import Result
from .models.classic import Classic
from .models.guaranteed import Guaranteed
from .models.gold_ball import GoldBall

_6_49_BASE_URL: Final[str] = "https://ca.lottonumbers.com"
_6_49_PAGE: Final[str] = "/lotto-649"
_6_49_CLASSIC_FILE_PATH_URL: Final[str] = "https://www.playnow.com/resources/documents/downloadable-numbers/649.zip"
_6_49_GP_FILE_PATH_URL: Final[str] = "https://www.playnow.com/resources/documents/downloadable-numbers/649GPs.zip"

_DRAW_DATE_FIELD: Final[str] = "DRAW DATE"
_PRIZE_WON_FIELD: Final[str] = "PRIZE WON"
_NUMBER_DRAWN_FIELD: Final[str] = "NUMBER DRAWN"
_BALL_DRAWN_FIELD: Final[str] = "BALL DRAWN"
_IS_GOLD_BALL_DRAWN_FIELD: Final[str] = "IS GOLD BALL DRAWN"
_BONUS_NUMBER_FIELD: Final[str] = "BONUS NUMBER"
_NUMBERS_FIELDS: Final[str] = "NUMBERS"
_DATE_FORMAT: Final[str] = "%Y-%m-%d"

def extract_all_years() -> list[int]:
    """Return all 6/49 years played"""
    return _get_6_49_years()

def extract_649_results_by_year(year: int) -> list[Result]:
    """Return results by selected years"""
    zip_file_classic_response: Response = get(_6_49_CLASSIC_FILE_PATH_URL)
    zip_file_gp_response: Response = get(_6_49_GP_FILE_PATH_URL)

    if zip_file_classic_response.status_code != 200:
        raise Exception(f"An error occured while fetching the classic results for the year {year}. \n message: {zip_file_classic_response.text}")
    
    if zip_file_gp_response.status_code != 200:
        raise Exception(f"An error occured while fetching the guaranteed prize results for the year {year}. \n message: {zip_file_gp_response.text}")
    
    zip_file_classic = ZipFile(BytesIO(zip_file_classic_response.content))
    zip_file_gp = ZipFile(BytesIO(zip_file_gp_response.content))

    csv_file_classic = read_csv(zip_file_classic.open("649.csv"))
    csv_file_gp = read_csv(zip_file_gp.open("649GPs.csv"))

    csv_file_classic[_DRAW_DATE_FIELD] = to_datetime(csv_file_classic[_DRAW_DATE_FIELD], format=_DATE_FORMAT)
    csv_file_gp[_DRAW_DATE_FIELD] = to_datetime(csv_file_gp[_DRAW_DATE_FIELD], format=_DATE_FORMAT)

    csv_file_classic = csv_file_classic[csv_file_classic[_DRAW_DATE_FIELD].dt.year == year]
    csv_file_gp = csv_file_gp[csv_file_gp[_DRAW_DATE_FIELD].dt.year == year]

    classic_data = _process_classic_results(csv_file_classic)
    guaranteed_data = _process_guaranteed_data(csv_file_gp)
    gold_ball_data = _process_gold_baell_data(csv_file_gp)

    classic_data["RESULT"] = classic_data.apply(lambda row: _build_result(row, gold_ball_data, guaranteed_data), axis=1)

    return classic_data["RESULT"].tolist()

def extract_649_results_by_date(date: datetime.date) -> PrizeBreakdown:
    """Return the 6/49 result within a specific date"""
    date_string: Final[str] = date.strftime(_DATE_FORMAT)
    date_result_page: Response = get(f"{_6_49_BASE_URL}{_6_49_PAGE}/numbers/{date_string}")

    if date_result_page.status_code != 200:
        raise Exception(f"An error occured while fetching the results for the date {date_string}. \n message: {date_result_page.text}")
    
    html_content: BeautifulSoup = BeautifulSoup(date_result_page.text, "html.parser")
    table_breakdown_result: Final[ResultSet] = html_content.find("table")

    if table_breakdown_result is None:
        raise Exception(f"The prize breakdown results for the date {date_string} is not available.")

    tr_tags: Final[list[ResultSet]] = table_breakdown_result.tbody.find_all("tr")
    
    return _process_prize_breakdown_results(tr_tags)

def _get_6_49_years() -> list[int]:
    """Return all lotto 6/49 years played"""
    six_foyrty_nine_page: Response = get(f"{_6_49_BASE_URL}{_6_49_PAGE}/past-numbers")

    if six_foyrty_nine_page.status_code != 200:
        raise Exception(f"Unable to fetch the years results.\n message: {six_foyrty_nine_page.text}")

    html_content: BeautifulSoup = BeautifulSoup(six_foyrty_nine_page.text, "html.parser")

    years_tags = html_content.find('div', class_="dropdown").find_all("li")

    years: Final[list[int]] = []

    for year in years_tags:
        years.append(int(year.find("a").text))

    return years

def _process_classic_results(csv_file_classic: DataFrame) -> DataFrame:
    number_columns: Final[list[str]] = ["NUMBER DRAWN 1", "NUMBER DRAWN 2", "NUMBER DRAWN 3", "NUMBER DRAWN 4", "NUMBER DRAWN 5", "NUMBER DRAWN 6"]

    csv_file_classic[_PRIZE_WON_FIELD] = csv_file_classic.apply(lambda row: _get_classic_prize(row), axis=1)
    csv_file_classic[_NUMBERS_FIELDS] = csv_file_classic[number_columns].values.tolist() 
    
    return csv_file_classic.loc[:, [_DRAW_DATE_FIELD, _PRIZE_WON_FIELD, _NUMBERS_FIELDS, _BONUS_NUMBER_FIELD]]

def _process_guaranteed_data(csv_file_gp: DataFrame) -> DataFrame:
    csv_file_gp[_PRIZE_WON_FIELD] = csv_file_gp[_PRIZE_WON_FIELD].replace("[\$,]", "", regex=True).astype(float)
    csv_file_gp[_NUMBER_DRAWN_FIELD] = csv_file_gp[_NUMBER_DRAWN_FIELD].replace(" ", "", regex=True)

    guaranteed_data: DataFrame = csv_file_gp[csv_file_gp[_BALL_DRAWN_FIELD] == "Not Applicable"].groupby([_DRAW_DATE_FIELD, _PRIZE_WON_FIELD]).agg({_NUMBER_DRAWN_FIELD: _collect_number}).reset_index()
    return guaranteed_data.loc[:, [_DRAW_DATE_FIELD, _PRIZE_WON_FIELD, _NUMBER_DRAWN_FIELD]]

def _process_gold_baell_data(csv_file_gp: DataFrame) -> DataFrame:
    gold_ball_data: DataFrame = csv_file_gp[csv_file_gp[_BALL_DRAWN_FIELD] != "Not Applicable"]
    gold_ball_data.loc[:, [_IS_GOLD_BALL_DRAWN_FIELD]] = gold_ball_data[_BALL_DRAWN_FIELD] == "Gold"
    return gold_ball_data.loc[:, [_DRAW_DATE_FIELD, _PRIZE_WON_FIELD, _NUMBER_DRAWN_FIELD, _IS_GOLD_BALL_DRAWN_FIELD]]

def _get_classic_prize(row) -> float | None:
    """Return the 6/49 classic prize"""
    date: Final[str] = row[_DRAW_DATE_FIELD].strftime(_DATE_FORMAT)
    result_page: Final[Response] = get(f"{_6_49_BASE_URL}{_6_49_PAGE}/numbers/{date}")

    if result_page.status_code != 200:
        raise Exception(f"Unable to fetch the prize for the date {date}. \n message: {result_page.text}")
    
    html_content: BeautifulSoup = BeautifulSoup(result_page.text, "html.parser")
    table_body: Final[ResultSet] = html_content.find("tbody")

    if table_body is None:
        return None
    
    tr_tags: Final[list[ResultSet]] = table_body.find_all("tr")
    price: Final[str] = tr_tags[0].find("td", {"data-title": "Prize"}).text.strip().replace("$", "").replace(",", "")

    return float(price)

def _build_result(row, gold_ball_data: DataFrame, guaranteed_data: DataFrame) -> Result:
    """Return the 6/49 result"""
    date: Final[datetime.date] = row["DRAW DATE"]

    classic: Final[Classic] = Classic(numbers=row[_NUMBERS_FIELDS], bonus=row[_BONUS_NUMBER_FIELD], prize=row[_PRIZE_WON_FIELD])
    guaranteed: list[Guaranteed] | None = None
    gold_ball: GoldBall | None = None

    if not guaranteed_data[guaranteed_data[_DRAW_DATE_FIELD] == date].empty:
        guaranteed_value_df: Final[DataFrame] = guaranteed_data.loc[guaranteed_data[_DRAW_DATE_FIELD] == date, [_PRIZE_WON_FIELD, _NUMBER_DRAWN_FIELD]].rename(columns={_NUMBER_DRAWN_FIELD: "numbers", _PRIZE_WON_FIELD: "prize"})
        guaranteed = guaranteed_value_df.apply(lambda row: Guaranteed(numbers=row["numbers"], prize=row["prize"]), axis=1).tolist()
    
    if not gold_ball_data[gold_ball_data[_DRAW_DATE_FIELD] == date].empty:
        gold_ball_value_df: Final[DataFrame] = gold_ball_data.loc[gold_ball_data[_DRAW_DATE_FIELD] == date, [_PRIZE_WON_FIELD, _NUMBER_DRAWN_FIELD, _IS_GOLD_BALL_DRAWN_FIELD]].rename(columns={_NUMBER_DRAWN_FIELD: "number", _PRIZE_WON_FIELD: "prize", _IS_GOLD_BALL_DRAWN_FIELD: "isGoldBallDrawn"})
        gold_ball = GoldBall(**gold_ball_value_df.to_dict(orient="records")[0])

    return Result(date=date.strftime(_DATE_FORMAT), classic=classic, guaranteed=guaranteed, goldBall=gold_ball)

def _collect_number(series) -> list[str]:
    """Return the numbers"""
    return list(series)


def _process_prize_breakdown_results(tr_tags: list[ResultSet]) -> PrizeBreakdown:
    """Return the numbers matched"""
    free_play_ticket: Final[str] = "Free Play Ticket"
    next_gold_ball: Final[str] = "Next Gold Ball Jackpot"
    match_two: Final[str] = "Match 2"

    numbers_matched: Final[list[NumbersMatched]] = []

    tr_totals = tr_tags.pop()

    total_winners: int = 0
    total_prize_fund: float = 0.0

    for tr in tr_tags:
        td_tags = tr.find_all("td")
        match: str = _format_match(td_tags[0].text)

        if match == next_gold_ball:
            continue

        prize_per_winner: Final[float | str] = free_play_ticket if match == match_two else _format_prize_value(td_tags[1].text.strip())
        winners: Final[int | None] = _format_total_winners(td_tags[2].text)
        prize_fund: Final[float | None] = None if match == match_two else _format_prize_value(td_tags[3].text.strip())

        if winners is not None:
            total_winners += winners

        if prize_fund is not None:
            total_prize_fund += prize_fund

        numbers_matched.append(NumbersMatched(match=match, prize_per_winner=prize_per_winner, total_winners=winners, prize_fund=prize_fund))
    
    return PrizeBreakdown(summary=Summary(total_winners=total_winners, total_prize_fund=total_prize_fund), numbers_matched=numbers_matched)


def _format_match(match: str) -> str:
    """Return the match"""
    return match.strip().replace("\n", "").replace("\r", "").replace("\t", "")

def _format_total_winners(total_winners: str) -> int | None:
    """Return the total winners"""
    winner: str =  re.sub("[^\d]", "", total_winners.strip().replace(",", ""))

    if len(winner) == 0 or winner == "-":
        return None
    
    return int(winner)

def _format_prize_value(prize: str) -> float | None:
    """Return the prize value"""
    prize: str = re.sub("[^\d\.]", "", prize.strip().replace(",", "").replace("\n", "").replace("\r", "").replace("\t", ""))

    if len(prize) == 0 or prize == "-":
        return None

    return float(prize)