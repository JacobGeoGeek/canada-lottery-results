from pydantic import BaseModel, Field


class NumbersMatched(BaseModel):
    """Statistic Numbers Matched"""
    match: str = Field(..., alias="match")
    prize_per_winner: float | str | None = Field(..., alias="prizePerWinner")
    total_winners: int | None = Field(..., alias="totalWinners")
    prize_fund: float | None = Field(..., alias="prizeFund")

    class Config:
        """Config to convert snake_case to camelCase for JSON response Payload"""
        populate_by_name = True