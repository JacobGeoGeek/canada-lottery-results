from json import loads
from typing import Final
from sqlalchemy import Column

from src.common.models.numbers_matched import NumbersMatched

from .entities.lotto_max_results import LottoMaxResults

from .models.numbers import Numbers
from .models.prize_breakdown import PrizeBreakdown
from .models.summary import Summary

def build_lotto_max_numbers(data: list[LottoMaxResults]) -> list[Numbers]:
    """Build lotto max numbers"""
    return list(map(lambda x: Numbers(date=x.date, prize=x.prize, numbers=x.numbers, bonus=x.bonus), data))

def build_lotto_max_prize_breakdown(data: LottoMaxResults) -> PrizeBreakdown:
    """Build lotto max prize breakdown"""
    summary: Final[Summary] = _build_summary(data.summary)
    number_mached: Final[list[NumbersMatched]] = _build_match_numbers(data.numbers_matched)

    return PrizeBreakdown(summary=summary, numbers_matched=number_mached)

def build_lotto_max_numbers_matched(data: Column) -> list[NumbersMatched]:
    """Build lotto max numbers matched"""
    return _build_match_numbers(data)

def _build_summary(summary: Column) -> Summary:
    """Build summary"""
    summary_dict: Final[dict] = loads(summary)
    return Summary(**summary_dict)

def _build_match_numbers(numbers_matched: Column) -> list[NumbersMatched]:
    """Build match numbers"""
    result: Final[list[NumbersMatched]] = []
    
    for value in numbers_matched:
        match_dict = loads(value)
        result.append(NumbersMatched(**match_dict))

    return result