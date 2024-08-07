import datetime
import traceback
from typing import Final

from fastapi import HTTPException
from requests import Response
from src.games.game_repository import get_years_by_name, is_year_exist_by_name, save_new_year_by_name
from src.notification.email_sender import email_sender

from .daily_grand_external_data import extract_daily_grand_prize_breakdown, extract_daily_grand_result, fetch_daily_grand_result
from .daily_grand_factory import build_daily_grand_body_email, build_daily_grand_new_result, build_daily_grand_prize_breakdown, build_daily_grand_results
from .daily_grand_repository import get_daily_grand_numbers_by_date, get_daily_grand_numbers_by_year, save_daily_grand_result
from .entities.daily_grand_results import DailyGrandResults

from .models.prize_breakdown import PrizeBreakdown
from .models.result import Result

_GAME_NAME: Final[str] = "dailygrand"

def find_all_years() -> list[int]:
    """Return all Daily grand years"""
    return get_years_by_name(_GAME_NAME)

def find_daily_grand_results_by_year(year: int) -> list[Result]:
    """Return all daily grand results by year"""
    result: Final[list[DailyGrandResults]] = get_daily_grand_numbers_by_year(year)

    if len(result) == 0:
      raise HTTPException(status_code=400, detail=f"No lottery numbers were found for the year {year}")

    return build_daily_grand_results(result)

def find_daily_grand_result_by_date(date: datetime.date) -> PrizeBreakdown:
    """Return the daily grand result within a specific date"""
    result: Final[DailyGrandResults] = get_daily_grand_numbers_by_date(date)

    if result is None:
      raise HTTPException(status_code=400, detail=f"No lottery numbers were found for the date {date.strftime('%Y-%m-%d')}. The Daily Grand numbers are drawn on Monday and Thursday evenings.")
    
    return build_daily_grand_prize_breakdown(result)

def insert_new_daily_grand_result(date: datetime.date) -> None:
    """Insert new daily grand result"""
    try:
        if get_daily_grand_numbers_by_date(date) is not None:
            email_sender.notify("ERROR Daily Grand", f"The numbers for the date {date.strftime('%Y-%m-%d')} already exist")
            return

        response_data: Response = fetch_daily_grand_result(date)
        external_number_result: Final[Result] = extract_daily_grand_result(date, response_data)
        external_prize_breakdown: Final[PrizeBreakdown] = extract_daily_grand_prize_breakdown(response_data)
        
        year: Final[int] = date.year

        if not is_year_exist_by_name(_GAME_NAME, year):
            save_new_year_by_name(_GAME_NAME, year)
            email_sender.notify("New Year added to Daily Grand", f"New year {year} was added to the database")

        new_result: Final[DailyGrandResults] = build_daily_grand_new_result(external_number_result, external_prize_breakdown)
        save_daily_grand_result(new_result)
        
        email_sender.notify("New Daily Grand result added", build_daily_grand_body_email(new_result))
    except Exception:
        email_sender.notify("ERROR Daily Grand", f"An error occurred while trying to add a new result for the date {date.strftime('%Y-%m-%d')}. <br> Error: {traceback.format_exc().replace('\n', '<br>')}")
