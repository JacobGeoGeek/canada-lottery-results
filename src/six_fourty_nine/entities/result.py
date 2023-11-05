from pydantic import BaseModel, Field
import datetime

from .classic import Classic
from .gold_ball import GoldBall
from .guaranteed import Guaranteed

class Result(BaseModel):
    """Model represent numbers results for 6/49"""
    date: datetime.date = Field(..., alias="date")
    classic: Classic = Field(..., alias="classic")
    guaranteed: Guaranteed | None = Field(..., alias="guaranteed")
    gold_ball: GoldBall | None = Field(..., alias="goldBall")

    


