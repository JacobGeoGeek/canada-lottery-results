
from fastapi import APIRouter
from .six_fourty_nine_service import fing_all_years

router = APIRouter(
    prefix="/6-49",
    tags=["6-49"],
    responses={404: {"description": "Not Found"}, 500: {"description": "Internal server error"}}
)

@router.get("/years", response_model=list[int])
async def get_six_fourty_nine_years() -> list[int]:
    """Get all years from lotto 6/49"""
    return fing_all_years()