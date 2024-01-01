from pydantic import BaseModel, Field

class BonusDraw(BaseModel):
    numbers: list[int] = Field(..., alias="numbers")
    prize: float = Field(..., alias="prize")