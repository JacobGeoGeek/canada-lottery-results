

from pydantic import BaseModel, Field


class Guaranteed(BaseModel):
    number: str = Field(..., alias="number")
    price: float = Field(..., alias="price")