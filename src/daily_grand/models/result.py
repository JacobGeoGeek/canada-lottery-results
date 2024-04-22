import datetime
from pydantic import BaseModel, Field

from .bonus_draw import BonusDraw

class Result(BaseModel):
    """Model represent numbers results for Daily Grand"""
    date: datetime.date = Field(..., alias="date")
    numbers: list[int] = Field(..., alias="numbers")
    grand_number: int = Field(..., alias="grandNumber")
    prize: float = Field(..., alias="prize")
    bonuses_draw: list[BonusDraw] = Field(..., alias="bonusesDraw")