from pydantic import BaseModel, Field
from humps import camelize


class Summary(BaseModel):
    """General information on a lotto max result"""
    ticket_sold: int | None = Field(alias="ticketSold")
    total_sales: float | None = Field(alias="totalSale")
    total_winners: int = Field(..., alias="totalWinners")
    total_prize_fund: float = Field(..., alias="totalPrizeFund")
    winning_ratio: float | None = Field(alias="winningRatio")
    sales_difference_previous_draw: str = Field(..., alias="saleDifferencePreviousDraw")

    class Config:
        """Config to convert snake_case to camelCase for JSON response Payload"""
        alias_generator = camelize
        allow_population_by_field_name = True
