from pydantic import BaseModel, Field

class Guaranteed(BaseModel):
    numbers: list[str] = Field(..., alias="numbers")
    prize: float = Field(..., alias="prize")