import datetime
from typing import Final

from fastapi import HTTPException
from sqlalchemy import Column
from src.common.models.numbers_matched import NumbersMatched
from src.games.game_repository import get_years_by_name
from .entities.lotto_max_results import LottoMaxResults
from .lottomax_repository import get_lotto_numbers_by_year, get_lotto_numbers_by_date, get_regions_numbers_matched_by_date
from .models.numbers import Numbers
from .models.prize_breakdown import PrizeBreakdown
from .models.region import Region
from .lottomax_factory import build_lotto_max_numbers, build_lotto_max_prize_breakdown, build_lotto_max_numbers_matched
from .lottomax_external_data import extract_lotto_result


def find_all_years() -> list[int]:
    """Find all years from lotto max"""
    return get_years_by_name("lottomax")

def find_lotto_numbers_by_year(year: int) -> list[Numbers]:
    """Find lotto numbers by year"""
    year_results: list[LottoMaxResults] = get_lotto_numbers_by_year(year)
    # TODO check if the results for the year contain the latest results. if not then update the database
    
    if len(year_results) == 0:
        raise HTTPException(status_code=404, detail="The numbers for the year were not found")
    
    return build_lotto_max_numbers(year_results)

def find_lotto_result(date: datetime.date) -> PrizeBreakdown:
    """Find lotto result by date"""
    lotto_max_result: LottoMaxResults = get_lotto_numbers_by_date(date)

    # TODO - If not found in the database, then call the external data and save it to the database
    if lotto_max_result is None:
       external_result: Final[PrizeBreakdown] = extract_lotto_result(date)
       
       if external_result is None:
            raise HTTPException(status_code=404, detail="The numbers for the date were not found")

       return external_result

    return build_lotto_max_prize_breakdown(lotto_max_result)

def find_lotto_result_by_date_and_region(date: datetime.date, region: Region) -> list[NumbersMatched]:
    """Find lotto result by date and region"""
    number_matched: LottoMaxResults = _get_results_by_region_and_date(date, region)

    #TODO - If not found in the database, then call the external data and save it to the database
    if number_matched is None:
        raise HTTPException(status_code=404, detail="The numbers matched for the region and date were not found")
    
    return build_lotto_max_numbers_matched(number_matched)


def _get_results_by_region_and_date(date: datetime.date, region: Region) -> Column:
    """Get results by region and date"""
    regions_number_matched: LottoMaxResults = get_regions_numbers_matched_by_date(date)

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