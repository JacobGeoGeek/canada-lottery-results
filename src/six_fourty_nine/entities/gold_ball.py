from pydantic import BaseModel, Field

class GoldBall(BaseModel):
    number: str = Field(..., alias="number")
    price: float = Field(..., alias="price")