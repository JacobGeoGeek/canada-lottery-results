from pydantic import BaseModel, Field

from .detail_breakdown import DetailBreakDown

class PrizeBreakdown(BaseModel):
    """Model represent prize breakdown for daily grand"""
    mainBreakdown: DetailBreakDown = Field(..., alias="mainBreakdown")
    bonusesBreakdown: DetailBreakDown | None = Field(..., alias="bonusesBreakdown")