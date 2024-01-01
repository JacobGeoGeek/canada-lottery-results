from pydantic import BaseModel, Field

from src.common.entities.numbers_matched import NumbersMatched
from src.common.entities.summary import Summary

class DetailBreakDown(BaseModel):
    """Model represent main breakdown for daily grand"""
    summary: Summary = Field(..., alias="summary")
    numbers_matched: list[NumbersMatched] = Field(..., alias="numbersMatched")

    class Config:
        """Config to convert snake_case to camelCase for JSON response Payload"""
        populate_by_name = True