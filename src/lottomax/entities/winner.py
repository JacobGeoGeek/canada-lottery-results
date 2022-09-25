from pydantic import BaseModel, Field
from .location import Location

class Winner(BaseModel):
    """Number of winner for each Match"""
    total: int = Field(..., alias="total")
    location: list[Location] = Field(..., alias="location")
