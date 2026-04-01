
from datetime import datetime
from pydantic import BaseModel, Field

from .max_million import MaxMillion

class Result(BaseModel):
    """Model represent numbers results for Western Max"""
    date: datetime.date = Field(..., alias="date")
    numbers: list[int] = Field(..., alias="numbers")
    bonus: int = Field(..., alias="bonus")
    prize: float = Field(..., alias="prize")
    # max_millions: list[MaxMillion] = Field(..., alias="maxMillions") TODO: Check How to get the max_millions resuls.