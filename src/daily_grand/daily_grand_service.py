import datetime
from typing import Final

from fastapi import HTTPException
from src.games.game_repository import get_years_by_name

from .daily_grand_factory import build_daily_grand_prize_breakdown, build_daily_grand_results
from .daily_grand_repository import get_daily_grand_numbers_by_date, get_daily_grand_numbers_by_year
from .entities.daily_grand_results import DailyGrandResults

from .models.prize_breakdown import PrizeBreakdown
from .models.result import Result

def find_all_years() -> list[int]:
    """Return all Daily grand years"""
    return get_years_by_name("dailygrand")

def find_daily_grand_results_by_year(year: int) -> list[Result]:
    """Return all daily grand results by year"""
    result: Final[list[DailyGrandResults]] = get_daily_grand_numbers_by_year(year)

    if len(result) == 0:
      raise HTTPException(status_code=404, detail="Year not found")

    return build_daily_grand_results(result)

def find_daily_grand_result_by_date(date: datetime.date) -> PrizeBreakdown:
    """Return the daily grand result within a specific date"""
    result: Final[DailyGrandResults] = get_daily_grand_numbers_by_date(date)

    if result is None:
      raise HTTPException(status_code=404, detail="Date not found")
    
    return build_daily_grand_prize_breakdown(result)