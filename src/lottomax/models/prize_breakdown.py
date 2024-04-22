from pydantic import BaseModel, Field

from src.common.models.numbers_matched import NumbersMatched
from .summary import Summary

class PrizeBreakdown(BaseModel):
    """Model represent prize statistic"""
    summary: Summary = Field(..., alias="summary")
    numbers_matched: list[NumbersMatched] = Field(..., alias="numbersMatched")

    class Config:
        """Config to convert snake_case to camelCase for JSON response Payload"""
        populate_by_name = True