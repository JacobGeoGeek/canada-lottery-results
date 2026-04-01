

from typing import Final
from src.common.models.detail_breakdown import DetailBreakDown
from .entities import WesternMaxResults
from .models.result import Result
from .models.prize_breakdown import PrizeBreakdown


def build_western_max_results(data: list[WesternMaxResults]) -> list[Result]:
    """Build Western Max results from database entities"""
    result: list[Result] = list(map(
        lambda item: Result(
            date=item.date,
            numbers=item.numbers,
            bonus=item.bonus,
            prize=item.prize,
            # max_millions=[MaxMillion(**mm) for mm in item.max_million_breakdown]  # TODO: Uncomment when MaxMillion model is defined
        ), data))
    
    return sorted(result, key=lambda x: x.date, reverse=True)

def build_western_max_prize_breakdown(data: WesternMaxResults) -> PrizeBreakdown:
    """Build Western Max prize breakdown from database entity"""
    main_breakdown: Final[DetailBreakDown] = DetailBreakDown(**data.main_breakdown)
    max_millions_breakdown: Final[DetailBreakDown | None] = DetailBreakDown(**data.max_million_breakdown) if data.max_million_breakdown else None

    return PrizeBreakdown(mainBreakdown=main_breakdown, maxMillionsBreakdown=max_millions_breakdown)
