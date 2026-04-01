
from pydantic import BaseModel, Field


class MaxMillion(BaseModel):
    """Model represent Max Million numbers for Western Max"""
    numbers: list[int] = Field(..., alias="numbers")
    winners: int = Field(..., alias="winners")
    prize: float = Field(..., alias="prize")
   