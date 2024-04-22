from datetime import date
from pydantic import BaseModel

class Numbers(BaseModel):
    """Model represent numbers results"""
    date: date
    prize: float
    numbers: list[int]
    bonus: int
