
from typing import Final
from fastapi import APIRouter, Path

from .entities.result import Result
from .six_fourty_nine_service import fing_all_years, find_649_results_by_year

router = APIRouter(
    prefix="/6-49",
    tags=["6-49"],
    responses={404: {"description": "Not Found"}, 500: {"description": "Internal server error"}}
)

_649_YEARS: Final[list[int]] = fing_all_years()
_649_START_YEAR: Final[int] = min(_649_YEARS)
_649_LAST_YEAR: Final[int] = max(_649_YEARS)

@router.get("/years", response_model=list[int])
async def get_six_fourty_nine_years() -> list[int]:
    """Get all years from lotto 6/49"""
    return _649_YEARS

@router.get("/years/{year}", response_model=list[Result])
async def get_six_fourty_nine_result_by_year(year: int = Path(
        title="The year of lotto 6/49 results to get",
        ge=_649_START_YEAR,
        le=_649_LAST_YEAR
)):
    """Get the lotto 6/49 numbers result by year"""
    return find_649_results_by_year(year)