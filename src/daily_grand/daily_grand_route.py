import datetime
from typing import Final
from fastapi import APIRouter, Path

from .models.prize_breakdown import PrizeBreakdown

from .models.result import Result
from .daily_grand_service import find_all_years, find_daily_grand_results_by_year, find_daily_grand_result_by_date

router = APIRouter(
    prefix="/daily-grand",
    tags=["daily-grand"],
    responses={404: {"description": "Not Found"}, 500: {"description": "Internal server error"}}
)

_DAILY_GRAND_YEARS: Final[list[int]] = find_all_years()
_DAILT_GRAND_START_YEAR: Final[int] = min(_DAILY_GRAND_YEARS)
_DAILY_GRAND_LAST_YEAR: Final[int] = max(_DAILY_GRAND_YEARS)

@router.get("/years", response_model=list[int])
async def get_daily_grand_years() -> list[int]:
    """Get all years from daily grand"""
    return _DAILY_GRAND_YEARS

@router.get("/years/{year}", response_model=list[Result])
async def get_daily_grand_result_by_year(year: int = Path(
        title="The year of daily grand results to get",
        ge=_DAILT_GRAND_START_YEAR,
        le=_DAILY_GRAND_LAST_YEAR
)):
    """Get the daily grand numbers result by year"""
    return find_daily_grand_results_by_year(year)

@router.get("/results/{date}", response_model=PrizeBreakdown)
async def get_daily_grand_result_by_date(
    date: datetime.date = Path(
        title="The date to view the winning numbers and prize payouts that took place"
    )):
    """Get the winning numbers and prise payouts for a specific date"""
    return find_daily_grand_result_by_date(date)