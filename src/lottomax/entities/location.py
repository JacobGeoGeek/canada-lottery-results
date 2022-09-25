from pydantic import BaseModel

class Location(BaseModel):
    """Winner Location"""
    region: str
    total: int
