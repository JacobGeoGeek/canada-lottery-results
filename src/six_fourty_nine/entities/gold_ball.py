from pydantic import BaseModel, Field

class GoldBall(BaseModel):
    number: str = Field(..., alias="number")
    prize: float = Field(..., alias="prize")