

from pydantic import BaseModel, Field


class Classic(BaseModel):
    """Model represent classic numbers results for 6/49"""
    numbers: list[int] = Field(..., alias="numbers")
    bonus: int = Field(..., alias="bonus")
    price: float | None = Field(..., alias="price")