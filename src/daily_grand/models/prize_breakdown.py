from pydantic import BaseModel, Field

from src.common.models.detail_breakdown import DetailBreakDown

class PrizeBreakdown(BaseModel):
    """Model represent prize breakdown for daily grand"""
    main_breakdown: DetailBreakDown = Field(..., alias="mainBreakdown")
    bonuses_breakdown: DetailBreakDown | None = Field(..., alias="bonusesBreakdown")