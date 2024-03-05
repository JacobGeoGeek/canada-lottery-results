import datetime

from fastapi import HTTPException

from .six_fourty_nine_factory import build_649_prize_breakdown, build_649_results

from .entities.six_fourty_nine_results import SixFourtyNineResults

from .models.prize_breakdown import PrizeBreakdown
from .models.result import Result

from src.games.game_repository import get_years_by_name
from .sixe_fourty_nine_repository import get_649_numbers_by_year, get_649_numbers_by_date

def find_all_years() -> list[int]:
    """Return all 6/49 years"""
    return get_years_by_name("sixfourtynine")

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
    
