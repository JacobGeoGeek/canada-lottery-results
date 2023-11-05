from pydantic import BaseModel, Field

class Guaranteed(BaseModel):
    number: str = Field(..., alias="number")
    prize: float = Field(..., alias="prize")