
from pydantic import BaseModel, Field


class MainPrize(BaseModel):
   """Model represent main prize for Western Max"""
   numbers: list[int] = Field(..., alias="numbers")
   bonus: int = Field(..., alias="bonus")
   prize: float = Field(..., alias="prize")