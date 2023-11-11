from pydantic import BaseModel, Field

class Summary(BaseModel):
    """Model represent total winners and total prize fund"""
    total_winners: int = Field(..., alias="totalWinners")
    total_prize_fund: float = Field(..., alias="totalPrizeFund")

    class Config:
        """Config to convert snake_case to camelCase for JSON response Payload"""
        populate_by_name = True