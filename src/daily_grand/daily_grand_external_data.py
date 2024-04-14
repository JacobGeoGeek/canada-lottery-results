import datetime
from typing import Final
from requests import get, Response
from zipfile import ZipFile
from io import BytesIO
from pandas import read_csv, DataFrame, to_datetime

from src.common.models.numbers_matched import NumbersMatched
from src.common.models.summary import Summary

from .models.prize_breakdown import PrizeBreakdown
from .models.detail_breakdown import DetailBreakDown
from .models.bonus_draw import BonusDraw
from .models.result import Result

_DAILY_GRAND_BASE_URL: Final[str] = "https://www.playnow.com"
_RESULT_FILE_PATH: Final[str] = "/resources/documents/downloadable-numbers/DailyGrand.zip"
_FILE_NAME: Final[str] = "DailyGrand.csv"
_DATE_FORMAT: Final[str] = "%Y-%m-%d"

_PRIZE_TYPE_ANNUITY: Final[str] = "annuity"

def extract_all_years() -> list[int]:
    """Return all daily grand years played"""
    draw_date_column: Final[str] = "DRAW DATE"

    response: Response = get(f"{_DAILY_GRAND_BASE_URL}{_RESULT_FILE_PATH}")

    if response.status_code != 200:
        raise Exception(f"An error occured while fetching the years \n message: {response.text}")
    
    zip_file = ZipFile(BytesIO(response.content))
    csv_file: Final[DataFrame] = read_csv(zip_file.open(_FILE_NAME))
    csv_file[draw_date_column] = to_datetime(csv_file[draw_date_column], format=_DATE_FORMAT)

    return csv_file[draw_date_column].dt.year.unique().tolist()

def extract_daily_grand_results_by_years(year: int) -> list[Result]:
    """Return results by selected years"""
    zip_file_response: Response = get(f"{_DAILY_GRAND_BASE_URL}{_RESULT_FILE_PATH}")

    if zip_file_response.status_code != 200:
        raise Exception(f"An error occured while fetching the results for the year {year} \n message: {zip_file_response.text}")

    zip_file = ZipFile(BytesIO(zip_file_response.content))
    csv_file: DataFrame = read_csv(zip_file.open(_FILE_NAME))
    csv_file["DRAW DATE"] = to_datetime(csv_file["DRAW DATE"], format=_DATE_FORMAT)

    csv_file = csv_file[(csv_file["DRAW DATE"].dt.year == year) & (csv_file["PRIZE DIVISION"] == 0)]
    csv_file = csv_file.sort_values(by=["DRAW DATE"], ascending=False)

    csv_file["JSON"] = csv_file.apply(lambda row: _build_result(row), axis=1)

    return csv_file["JSON"].tolist()

def extract_daily_grand_result_by_date(date: datetime.date) -> PrizeBreakdown:
    """Return the daily grand result within a specific date"""
    detail_page: Response = get(f"{_DAILY_GRAND_BASE_URL}/services2/lotto/draw/dgrd/{date.strftime(_DATE_FORMAT)}")

    if detail_page.status_code != 200:
        raise Exception(f"The date {date} does not exist within the daily grand results \n message: {detail_page.text}")
    
    game_breakdown: Final[list[dict]] = detail_page.json()["gameBreakdown"]
    main_breakdown: Final[DetailBreakDown] = _build_main_breakdown(list(filter(lambda breakdown: breakdown["prizeDiv"] != 20, game_breakdown)))
    bonus_breakdown: Final[DetailBreakDown | None] = _build_bonus_breakdown(list(filter(lambda breakdown: breakdown["prizeDiv"] == 20, game_breakdown)))

    return PrizeBreakdown(mainBreakdown=main_breakdown, bonusesBreakdown=bonus_breakdown)

def _build_result(row) -> Result:
    """Return the grand price for the selected date"""
    date: Final[str] = row["DRAW DATE"].strftime(_DATE_FORMAT)
    result_page: Final[Response] = get(f"{_DAILY_GRAND_BASE_URL}/services2/lotto/draw/dgrd/{date}")

    if result_page.status_code != 200:
        raise Exception(f"An error occured while fetching the results for the date {date} \n message: {result_page.text}")
    
    result_payload: Final[dict] = result_page.json()
    
    numbers: list[int] = result_payload["drawNbrs"]
    grand_number: int = result_payload["bonusNbr"]
    prize: str = result_payload["gameBreakdown"][0]["prizeAmount"]

    bonus_draw_details: list[dict] = result_payload["bonusDrawDetails"]

   # remove duplication bonus_draw details by using the key seqNbr
    bonus_draw_details = {v['seqNbr']:v for v in bonus_draw_details}.values()

    bonuses_draw: list[BonusDraw] = list(map(lambda bonus: BonusDraw(numbers=bonus["drawNbrs"], prize=bonus["prizeAmount"]), result_payload["bonusDrawDetails"]))

    return Result(date=row["DRAW DATE"], numbers=numbers, grandNumber=grand_number, prize=prize, bonusesDraw=bonuses_draw)

def _build_main_breakdown(main_breakdown: list[dict]) -> DetailBreakDown:
    """Return the detail breakdown"""
    numbers_matched: Final[list[NumbersMatched]] = []
    summary_total_winners: int = 0
    summary_total_prize_fund: float = 0.0

    matches_processed: set[str] = set()

    for breakdown in main_breakdown:
        match: Final[str] = breakdown["abbrev"]

        if match not in matches_processed:
            total_winners: Final[int] = breakdown["winnersTotal"]
            prize_per_winner: Final[float | str] = _get_detail_prize_per_winner(breakdown)
            prize_fund: Final[float | None] = _get_prize_fund(breakdown)
    
            summary_total_winners += total_winners

            if prize_fund != None:
                summary_total_prize_fund += prize_fund
            
            matches_processed.add(match)

            numbers_matched.append(NumbersMatched(match=match, prizePerWinner=prize_per_winner, totalWinners=total_winners, prizeFund=prize_fund))
    
    return DetailBreakDown(summary=Summary(totalWinners=summary_total_winners, totalPrizeFund=summary_total_prize_fund), numbersMatched=numbers_matched)

def _build_bonus_breakdown(bonus_breakdown: list[dict]) -> DetailBreakDown | None:
    """Return the detail breakdown for the bonus draw"""
    if len(bonus_breakdown) == 0:
        return None
    
    numbers_matched: Final[list[NumbersMatched]] = []
    summary_total_winners: int = 0
    summary_total_prize_fund: float = 0.0

    sequence_number_processed: set[int] = set()

    for breakdown in bonus_breakdown:
        match: Final[str] = breakdown["abbrev"]
        sequence_number: Final[int] = breakdown["seqNbr"]

        if sequence_number not in sequence_number_processed:
            total_winners: Final[int] = breakdown["winnersTotal"]
            prize_per_winner: Final[float | str] = _get_detail_prize_per_winner(breakdown)
            prize_fund: Final[float | None] = _get_prize_fund(breakdown)
    
            summary_total_winners += total_winners

            if prize_fund != None:
                summary_total_prize_fund += prize_fund
            
            sequence_number_processed.add(sequence_number)

            numbers_matched.append(NumbersMatched(match=match, prizePerWinner=prize_per_winner, totalWinners=total_winners, prizeFund=prize_fund))

    return DetailBreakDown(summary=Summary(totalWinners=summary_total_winners, totalPrizeFund=summary_total_prize_fund), numbersMatched=numbers_matched)

def _get_detail_prize_per_winner(breakdown: dict) -> str | float:
    """Return the prize details"""
    if breakdown["prizeType"] == "":
        return "Free Play"
    elif breakdown["prizeType"] == _PRIZE_TYPE_ANNUITY and breakdown["winnersTotal"] > 1:
        return breakdown["prizeAmount"] / breakdown["winnersTotal"]
    elif breakdown["prizeType"] == "annuity" and breakdown["annuityDetails"] != None:
        return f"{_get_annuity_details(breakdown['annuityDetails'])} or lump sum of ${breakdown['prizeAmount']}"
    else:
        return breakdown["prizeAmount"]

def _get_prize_fund(breakdown: dict) -> float | None:
    """Return the prize fund"""
    if breakdown["prizeType"] == "":
        return None
    elif breakdown["prizeType"] == _PRIZE_TYPE_ANNUITY and breakdown["winnersTotal"] >= 1:
        return breakdown["prizeAmount"]
    else :
        return breakdown["prizeAmount"] * breakdown["winnersTotal"]

def _get_annuity_details(annuity_details: dict) -> str:
    """Return the annuity details"""
    return f"${annuity_details['annuityAmount']} a {annuity_details['annuityFrequency']} for {annuity_details['annuityDuration']}"