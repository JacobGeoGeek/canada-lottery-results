from pydantic import BaseModel, Field
from humps import camelize

from .numbers_matched import NumbersMatched
from .summary import Summary

class PrizeBreakdown(BaseModel):
    """Model represent prize statistic"""
    summary: Summary = Field(..., alias="summary")
    numbers_matched: list[NumbersMatched] = Field(..., alias="numbersMatched")

    class Config:
        """Config to convert snake_case to camelCase for JSON response Payload"""
        alias_generator = camelize
        allow_population_by_field_name = True
