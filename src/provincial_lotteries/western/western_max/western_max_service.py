
import datetime
import traceback
from typing import Final

from fastapi import HTTPException
from requests import Response


from src.games.game_repository import get_years_by_name
from src.notification import email_sender
from .western_max_external_data import fetch_western_max_result
from .western_max_factory import build_western_max_prize_breakdown, build_western_max_results
from .western_max_repository import get_western_max_numbers_by_date, get_western_max_numbers_by_year
from .entities import WesternMaxResults

from .models.result import Result
from .models.prize_breakdown import PrizeBreakdown

_GAME_NAME: Final[str] = "western_max"

def final_all_years() -> list[int]:
    """Find all years from Western Max"""
    return get_years_by_name(_GAME_NAME)

def find_western_max_numbers_by_year(year: int) -> list[Result]:
    """Find Western Max numbers by year"""
    result: Final[list[WesternMaxResults]] = get_western_max_numbers_by_year(year)

    if len(result) == 0:
        raise HTTPException(status_code=400, detail=f"No lottery numbers were found for the year {year}")
    
    return build_western_max_results(result)

def find_western_max_by_date(date: datetime.date) -> PrizeBreakdown:
    """Find Western Max numbers by date"""
    result: Final[WesternMaxResults] = get_western_max_numbers_by_date(date)

    if result is None:
        raise HTTPException(status_code=400, detail=f"No lottery numbers were found for the date {date.strftime('%Y-%m-%d')}. The Western Max numbers are drawn on Wednesday evenings.")
    
    return build_western_max_prize_breakdown(result)

def insert_new_western_max_result(date: datetime.date) -> None:
    """Insert new Western Max result"""
    try:
        if get_western_max_numbers_by_date(date) is not None:
            email_sender.notify("ERROR Western Max", f"The numbers for the date {date.strftime('%Y-%m-%d')} already exist")
            return
        
        # Fetch and process the new result data here
        response_data: Response = fetch_western_max_result(date)
        # external_number_result: Final[Result] = extract_western_max_result(date, response_data)
        # external_prize_breakdown: Final[PrizeBreakdown] = extract_western_max_prize_breakdown(response_data)

        # year: Final[int] = date.year
        # if not is_year_exist_by_name(_GAME_NAME, year):
        #     save_new_year_by_name(_GAME_NAME, year)
        #     email_sender.notify("New Year added to Western Max", f"New year {year} was added to the database")


        # Build and save the new result
        # new_result: Final[WesternMaxResults] = build_western_max_new_result(external_number_result, external_prize_breakdown)
        # save_western_max_result(new_result)
        raise NotImplementedError("Western Max result insertion is not implemented yet")
    except HTTPException:
        email_sender.email_sender.notify("ERROR Western Max", f"An error occurred while inserting the new Western Max result for {date.strftime('%Y-%m-%d')}. <br> Error: {traceback.format_exc().replace('\n', '<br>')} ")