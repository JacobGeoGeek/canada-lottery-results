
from dataclasses import Field
from pydantic import BaseModel

from src.common.models.detail_breakdown import DetailBreakDown
from .max_million import MaxMillion


class PrizeBreakdown(BaseModel):
   """Model represent prize breakdown for Western Max"""
   main_breakdown: DetailBreakDown = Field(..., alias="mainBreakdown")
   max_millions_breakdown: list[MaxMillion] = Field(..., alias="maxMillionsBreakdown")