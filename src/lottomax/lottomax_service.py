import datetime
import traceback
from typing import Final

from fastapi import HTTPException
from sqlalchemy import Column
from src.common.models.numbers_matched import NumbersMatched
from src.games.game_repository import get_years_by_name, is_year_exist_by_name, save_new_year_by_name
from src.notification.email_sender import email_sender
from .entities.lotto_max_results import LottoMaxResults
from .lottomax_repository import get_lotto_numbers_by_year, get_lotto_numbers_by_date, get_regions_numbers_matched_by_date, save_lotto_max_result
from .models.numbers import Numbers
from .models.prize_breakdown import PrizeBreakdown
from .models.region import Region
from .lottomax_factory import build_lotto_max_body_email, build_lotto_max_numbers, build_lotto_max_prize_breakdown, build_lotto_max_numbers_matched, build_lotto_max_result
from .lottomax_external_data import extract_lotto_numbers_by_year, extract_lotto_result, extract_lotto_result_by_date_and_region

_GAME_NAME: Final[str] = "lottomax"

def find_all_years() -> list[int]:
    """Find all years from lotto max"""
    return get_years_by_name(_GAME_NAME)

def find_lotto_numbers_by_year(year: int) -> list[Numbers]:
    """Find lotto numbers by year"""
    year_results: list[LottoMaxResults] = get_lotto_numbers_by_year(year)
        
    if len(year_results) == 0:
        raise HTTPException(status_code=404, detail="The numbers for the year were not found")
    
    return build_lotto_max_numbers(year_results)

def find_lotto_result(date: datetime.date) -> PrizeBreakdown:
    """Find lotto result by date"""
    lotto_max_result: LottoMaxResults = get_lotto_numbers_by_date(date)

    if lotto_max_result is None:
         raise HTTPException(status_code=404, detail="The numbers for the date were not found")

    return build_lotto_max_prize_breakdown(lotto_max_result)

def find_lotto_result_by_date_and_region(date: datetime.date, region: Region) -> list[NumbersMatched]:
    """Find lotto result by date and region"""
    number_matched: LottoMaxResults = _get_results_by_region_and_date(date, region)

    if number_matched is None:
        raise HTTPException(status_code=404, detail="The numbers matched for the region and date were not found")
    
    return build_lotto_max_numbers_matched(number_matched)

def insert_new_lotto_result(date: datetime.date) -> None:
    """Insert new lotto result"""
    try:
        if get_lotto_numbers_by_date(date) is not None:
            email_sender.notify("ERROR Lotto Max", f"The numbers for the date {date.strftime('%Y-%m-%d')} already exist")
            return

        year: Final[int] = date.year
        external_number_result: Final[Numbers] = next(filter(lambda number: number.date == date, extract_lotto_numbers_by_year(year)), None)
        external_result: Final[PrizeBreakdown] = extract_lotto_result(date)

        if external_number_result is None:
            email_sender.notify("ERROR Lotto Max numbers", f"The numbers for the date {date.strftime('%Y-%m-%d')} were not found")
            return
    
        if external_result is None:
            email_sender.notify("ERROR Lotto Max prize breakdown", f"The prize breakdown for the date {date.strftime('%Y-%m-%d')} were not found")
            return
        
        if not is_year_exist_by_name(_GAME_NAME, year):
            save_new_year_by_name(_GAME_NAME, year)
            email_sender.notify("New year added to Lotto Max" f"The year {year} was added to the database")

        result_quebec: Final[list[NumbersMatched]] = extract_lotto_result_by_date_and_region(date, Region.QUEBEC)
        result_ontario: Final[list[NumbersMatched]] = extract_lotto_result_by_date_and_region(date, Region.ONTARIO)
        result_atlantic: Final[list[NumbersMatched]] = extract_lotto_result_by_date_and_region(date, Region.ATLANTIC)
        result_western_canada: Final[list[NumbersMatched]] = extract_lotto_result_by_date_and_region(date, Region.WESTERN_CANADA)
        result_british_columbia: Final[list[NumbersMatched]] = extract_lotto_result_by_date_and_region(date, Region.BRITISH_COLUMBIA)

        lotto_max_result: Final[LottoMaxResults] = build_lotto_max_result(external_number_result, external_result, result_quebec, result_ontario, result_atlantic, result_western_canada, result_british_columbia)
        save_lotto_max_result(lotto_max_result)

        email_sender.notify("New Lotto Max result", build_lotto_max_body_email(lotto_max_result))
    except Exception:
        email_sender.notify("ERROR Lotto Max", f"An error occurred while inserting the lotto max result for the date {date.strftime('%Y-%m-%d')}.<br> Error: {traceback.format_exc().replace('\n', '<br>')}")

def _get_results_by_region_and_date(date: datetime.date, region: Region) -> Column:
    """Get results by region and date"""
    regions_number_matched: LottoMaxResults = get_regions_numbers_matched_by_date(date)

    if regions_number_matched is None:
        raise HTTPException(status_code=400, detail=f"The numbers matched for the date {date.strftime('%Y-%m-%d')} were not found")

    if region == Region.ATLANTIC:
        return regions_number_matched.numbers_matched_atlantic
    elif region == Region.BRITISH_COLUMBIA:
        return regions_number_matched.numbers_matched_british_columbia
    elif region == Region.ONTARIO:
        return regions_number_matched.numbers_matched_ontario
    elif region == Region.QUEBEC:
        return regions_number_matched.numbers_matched_quebec
    elif region == Region.WESTERN_CANADA:
        return regions_number_matched.numbers_matched_western_canada
    else:
        raise HTTPException(status_code=404, detail="The region was not found")