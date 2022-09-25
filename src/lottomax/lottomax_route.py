import datetime
from typing import Final
from fastapi import APIRouter, Path

from .models.region import Region

from .entities.numbers_matched import NumbersMatched
from .entities.prize_breakdown import PrizeBreakdown
from .entities.numbers import Numbers

from .lottomax_service import find_all_years, find_lotto_numbers_by_year, find_lotto_result, find_lotto_result_by_date_and_region

router = APIRouter(
    prefix="/lottomax",
    tags=["lottomax"],
    responses={404: {"description": "Not Found"}, 500: {"description": "Internal server error"}}
)

_LOTTOMAX_YEARS: Final[list[int]] = find_all_years()

_LOTTOMAX_START_YEAR: Final[int] = min(_LOTTOMAX_YEARS)
_LOTTOMAX_LAST_YEAR: Final[int] = max(_LOTTOMAX_YEARS)

@router.get("/years", response_model=list[int])
async def get_lotto_years() -> list[int]:
    """Get all years from lotto max"""
    return _LOTTOMAX_YEARS

@router.get("/{year}", response_model=list[Numbers])
async def get_lottomax_result_by_year(
    year: int = Path(
        title="The year of lotto max results to get",
        ge=_LOTTOMAX_START_YEAR,
        le=_LOTTOMAX_LAST_YEAR
        )):
    """Get the lotto max numbers result by year"""
    return find_lotto_numbers_by_year(year)

@router.get("results/{date}", response_model=PrizeBreakdown)
async def get_lottomax_result_by_date(
    date: datetime.date = Path(
        title="The date to view the winning numbers and prize payouts that took place"
    )):
    """Get the winning numbers and prisze payouts for a specific date"""
    return find_lotto_result(date)

@router.get("results/{date}/regions/{region}", response_model=list[NumbersMatched])
async def get_lottomax_result_by_date_and_location(
    date: datetime.date = Path(...,
        title="The date"
    ),
    region: Region = Path(..., title="The region")
    ):
    """Get the winning numbers and prisze payouts for a specific date and  Region"""
    return find_lotto_result_by_date_and_region(date, region)

