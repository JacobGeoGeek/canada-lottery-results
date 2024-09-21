from typing import Final
from sqlalchemy import Column

from src.common.models.numbers_matched import NumbersMatched

from .entities.lotto_max_results import LottoMaxResults

from .models.numbers import Numbers
from .models.prize_breakdown import PrizeBreakdown
from .models.summary import Summary

def build_lotto_max_numbers(data: list[LottoMaxResults]) -> list[Numbers]:
    """Build lotto max numbers"""
    result: Final[list[Numbers]] = list(map(lambda x: Numbers(date=x.date, prize=x.prize, numbers=x.numbers, bonus=x.bonus), data))
    return sorted(result, key=lambda x: x.date, reverse=True)

def build_lotto_max_prize_breakdown(data: LottoMaxResults) -> PrizeBreakdown:
    """Build lotto max prize breakdown"""
    summary: Final[Summary] = _build_summary(data.summary)
    number_mached: Final[list[NumbersMatched]] = _build_match_numbers(data.numbers_matched)

    return PrizeBreakdown(summary=summary, numbers_matched=number_mached)

def build_lotto_max_numbers_matched(data: Column) -> list[NumbersMatched]:
    """Build lotto max numbers matched"""
    return _build_match_numbers(data)

def build_lotto_max_result(number: Numbers, prize_breakdown: PrizeBreakdown, quebec: list[NumbersMatched], ontario: list[NumbersMatched], atlantic: list[NumbersMatched], western_canada: list[NumbersMatched], british_columbia: list[NumbersMatched]) -> LottoMaxResults:
    """Build lotto max result"""
    return LottoMaxResults(
        date=number.date,
        game_id=1,
        numbers=number.numbers,
        bonus=number.bonus,
        prize=number.prize,
        summary=prize_breakdown.summary.model_dump(mode="json"),
        numbers_matched=list(map(lambda x: x.model_dump(mode="json"), prize_breakdown.numbers_matched)),
        numbers_matched_quebec=_build_region_json(quebec),
        numbers_matched_ontario=_build_region_json(ontario),
        numbers_matched_atlantic=_build_region_json(atlantic),
        numbers_matched_western_canada=_build_region_json(western_canada),
        numbers_matched_british_columbia=_build_region_json(british_columbia)
    )

def build_lotto_max_body_email(data: LottoMaxResults) -> str:
    """Build lotto max body email"""
    return f"""
    <h1>Lotto Max Result</h1>
    <p>Date: {data.date}</p>
    <p>Numbers: {data.numbers}</p>
    <p>Bonus: {data.bonus}</p>
    <p>Prize: {data.prize}</p>
    <p>Summary:</p>
    <pre>{data.summary}</pre>
    <p>Numbers Matched:</p>
    <pre>{data.numbers_matched}</pre>
    <p>Numbers Matched Quebec:</p>
    <pre>{data.numbers_matched_quebec}</pre>
    <p>Numbers Matched Ontario:</p>
    <pre>{data.numbers_matched_ontario}</pre>
    <p>Numbers Matched Atlantic:</p>
    <pre>{data.numbers_matched_atlantic}</pre>
    <p>Numbers Matched Western Canada:</p>
    <pre>{data.numbers_matched_western_canada}</pre>
    <p>Numbers Matched British Columbia:</p>
    <pre>{data.numbers_matched_british_columbia}</pre>
    """

def _build_summary(summary: Column) -> Summary:
    """Build summary"""
    return Summary(**summary)

def _build_match_numbers(numbers_matched: Column) -> list[NumbersMatched]:
    """Build match numbers"""
    return list(map(lambda x: NumbersMatched(**x), numbers_matched))

def _build_region_json(data: list[NumbersMatched]) -> str:
    """Build region dict"""
    return list(map(lambda x: x.model_dump(mode="json"), data))