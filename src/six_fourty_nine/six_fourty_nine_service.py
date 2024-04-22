import datetime
import traceback
from typing import Final

from fastapi import HTTPException

from src.notification.email_sender import email_sender

from .six_fourty_nine_external_data import extract_649_results_by_date, extract_649_results_by_year
from .six_fourty_nine_factory import build_649_body_email, build_649_new_result, build_649_prize_breakdown, build_649_results

from .entities.six_fourty_nine_results import SixFourtyNineResults

from .models.prize_breakdown import PrizeBreakdown
from .models.result import Result

from src.games.game_repository import get_years_by_name, is_year_exist_by_name, save_new_year_by_name
from .sixe_fourty_nine_repository import get_649_numbers_by_year, get_649_numbers_by_date, save_649_result

_GAME_NAME: Final[str] = "sixfourtynine"

def find_all_years() -> list[int]:
    """Return all 6/49 years"""
    return get_years_by_name(_GAME_NAME)

def find_649_numbers_by_year(year: int) -> list[Result]:
    """Return 6/49 numbers by year"""
    year_results: list[SixFourtyNineResults] = get_649_numbers_by_year(year)

    if len(year_results) == 0:
        raise HTTPException(status_code=404, detail="The numbers for the year were not found")
    
    return build_649_results(year_results)

def find_649_by_date(date: datetime.date) -> PrizeBreakdown:
    """Return 6/49 numbers by date"""
    result: SixFourtyNineResults = get_649_numbers_by_date(date)

    if result is None:
        raise HTTPException(status_code=404, detail="The numbers for the date were not found")
    
    return build_649_prize_breakdown(result)

def insert_new_649_result(date: datetime.date) -> None:
    """Insert new 6/49 result"""
    try:
        if get_649_numbers_by_date(date) is not None:
         email_sender.notify("ERROR 6/49", f"The numbers for the date {date.strftime('%Y-%m-%d')} already exist.")
         return

        year: Final[int] = date.year
        external_number_result: Final[Result] = next(filter(lambda number: number.date == date, extract_649_results_by_year(year)), None)
        external_prize_breakdown: Final[PrizeBreakdown] = extract_649_results_by_date(date)

        if external_number_result is None:
            email_sender.notify("ERROR 6/49 numbers", f"The numbers for the date {date.strftime('%Y-%m-%d')} were not found.")
            return
        
        if external_prize_breakdown is None:
            email_sender.notify("ERROR 6/49 prize breakdown", f"The prize breakdown for the date {date.strftime('%Y-%m-%d')} were not found.")
            return

        if not is_year_exist_by_name(_GAME_NAME, year):
            save_new_year_by_name(_GAME_NAME, year)
            email_sender.notify("New 6/49 year", f"A new year {year} was added to the database.")

        new_result: Final[SixFourtyNineResults] = build_649_new_result(external_number_result, external_prize_breakdown)
        save_649_result(new_result)

        email_sender.notify("New 6/49 result", build_649_body_email(new_result))
    except Exception:
        email_sender.notify("ERROR 6/49", f"An error occurred while inserting the 6/49 result for the date {date.strftime('%Y-%m-%d')}.<br> Error: {traceback.format_exc().replace('\n', '<br>')}")