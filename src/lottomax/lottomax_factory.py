from json import loads, dumps
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

def build_lotto_max_result(number: Numbers, prize_breakdown: PrizeBreakdown, quebec: list[NumbersMatched], ontario: list[NumbersMatched], atlantic: list[NumbersMatched], western_canada: list[NumbersMatched], british_columbia: list[NumbersMatched]) -> LottoMaxResults:
    """Build lotto max result"""
    return LottoMaxResults(
        date=number.date,
        game_id=1,
        numbers=number.numbers,
        bonus=number.bonus,
        prize=number.prize,
        summary=prize_breakdown.summary.model_dump_json(),
        numbers_matched=list(map(lambda x: x.model_dump_json(), prize_breakdown.numbers_matched)),
        numbers_matched_quebec=_build_region_json(quebec),
        numbers_matched_ontario=_build_region_json(ontario),
        numbers_matched_atlantic=_build_region_json(atlantic),
        numbers_matched_western_canada=_build_region_json(western_canada),
        numbers_matched_british_columbia=_build_region_json(british_columbia)
    )

def build_lotto_max_body_email(data: LottoMaxResults) -> str:
    """Build lotto max body email"""
    indent_json: Final[int] = 4
    return f"""
    <h1>Lotto Max Result</h1>
    <p>Date: {data.date}</p>
    <p>Numbers: {data.numbers}</p>
    <p>Bonus: {data.bonus}</p>
    <p>Prize: {data.prize}</p>
    <p>Summary:</p>
    <pre>{dumps(data.summary, indent=indent_json)}</pre>
    <p>Numbers Matched:</p>
    <pre>{dumps(data.numbers_matched, indent=indent_json)}</pre>
    <p>Numbers Matched Quebec:</p>
    <pre>{dumps(data.numbers_matched_quebec, indent=indent_json)}</pre>
    <p>Numbers Matched Ontario:</p>
    <pre>{dumps(data.numbers_matched_ontario, indent=indent_json)}</pre>
    <p>Numbers Matched Atlantic:</p>
    <pre>{dumps(data.numbers_matched_atlantic, indent=indent_json)}</pre>
    <p>Numbers Matched Western Canada:</p>
    <pre>{dumps(data.numbers_matched_western_canada, indent=indent_json)}</pre>
    <p>Numbers Matched British Columbia:</p>
    <pre>{dumps(data.numbers_matched_british_columbia, indent=indent_json)}</pre>
    """

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

def _build_region_json(data: list[NumbersMatched]) -> list[str]:
    """Build region dict"""
    return list(map(lambda x: x.model_dump_json(), data))
