import datetime
from json import loads
from typing import Final

from sqlalchemy import Column

from .entities.daily_grand_results import DailyGrandResults

from .models.detail_breakdown import DetailBreakDown
from .models.result import Result
from .models.bonus_draw import BonusDraw
from .models.prize_breakdown import PrizeBreakdown

def build_daily_grand_results(data: list[DailyGrandResults]) -> list[Result]:
    """Build daily grand results"""
    results: list[Result] = []

    for value in data:
        date: datetime.date = value.date
        numbers: Final[int] = value.numbers
        grand_number: Final[int] = value.grand_number
        prize: Final[float] = value.prize
        bonuses_draw: Final[list[BonusDraw]] = _build_bonuses_draw(value.bonuses_draw)
        
        results.append(Result(date=date, numbers=numbers, grandNumber=grand_number, prize=prize, bonusesDraw=bonuses_draw))

    return results

def build_daily_grand_prize_breakdown(data: DailyGrandResults) -> PrizeBreakdown:
    """Build daily grand prize breakdown"""
    main_breakdown: Final[DetailBreakDown] = DetailBreakDown(**loads(data.main_breakdown))
    bonuses_breakdown: Final[DetailBreakDown | None] = DetailBreakDown(**loads(data.bonus_breakdown)) if data.bonus_breakdown else None 

    return PrizeBreakdown(mainBreakdown=main_breakdown, bonusesBreakdown=bonuses_breakdown)

def _build_bonuses_draw(data: Column) -> list[BonusDraw]:
    """Build bonuses draw"""
    bonuses_draw: list[BonusDraw] = []

    for value in data:
        bonus_draw_dict: Final[dict] = loads(value)
        bonuses_draw.append(BonusDraw(**bonus_draw_dict))

    return bonuses_draw