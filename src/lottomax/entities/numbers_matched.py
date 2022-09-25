from pydantic import BaseModel, Field
from humps import camelize

from .winner import Winner



class NumbersMatched(BaseModel):
    """Statistic Numbers Matched"""
    match: str = Field(..., alias="match")
    prize_per_winner: float | str = Field(..., alias="prizePerWinner")
    winner: Winner = Field(..., alias="winner")
    prize_fund: float | None = Field(alias="prizeFund")

    class Config:
        """Config to convert snake_case to camelCase for JSON response Payload"""
        alias_generator = camelize
        allow_population_by_field_name = True
