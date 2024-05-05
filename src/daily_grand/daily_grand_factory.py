import datetime
from json import loads, dumps
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

    return sorted(results, key=lambda x: x.date, reverse=True)

def build_daily_grand_prize_breakdown(data: DailyGrandResults) -> PrizeBreakdown:
    """Build daily grand prize breakdown"""
    main_breakdown: Final[DetailBreakDown] = DetailBreakDown(**loads(data.main_breakdown))
    bonuses_breakdown: Final[DetailBreakDown | None] = DetailBreakDown(**loads(data.bonus_breakdown)) if data.bonus_breakdown else None 

    return PrizeBreakdown(mainBreakdown=main_breakdown, bonusesBreakdown=bonuses_breakdown)

def build_daily_grand_new_result(number_result: Result, prize_breakdown: PrizeBreakdown) -> DailyGrandResults:
    """Build daily grand new result"""
    return DailyGrandResults(
        date=number_result.date,
        game_id=2,
        numbers=number_result.numbers,
        grand_number=number_result.grand_number,
        bonuses_draw=list(map(lambda bonus_draw: bonus_draw.model_dump_json(), number_result.bonuses_draw)),
        prize=number_result.prize,
        main_breakdown=prize_breakdown.main_breakdown.model_dump_json(),
        bonus_breakdown=prize_breakdown.bonuses_breakdown.model_dump_json() if prize_breakdown.bonuses_breakdown else None
    )

def build_daily_grand_body_email(data: DailyGrandResults) -> str:
    """Build daily grand body email"""
    json_indent: Final[int] = 4
    return f"""
    <h1>Daily Grand Result</h1>
    <p>Date: {data.date}</p>
    <p>Numbers: {data.numbers}</p>
    <p>Grand Number: {data.grand_number}</p>
    <p>Prize: {data.prize}</p>
    <p>Main Breakdown:</p>
    <pre>{dumps(data.main_breakdown, indent=json_indent)}</pre>
    <p>Bonus Breakdown:</p>
    <pre>{dumps(data.bonus_breakdown, indent=json_indent)}</pre>
    <p>Bonuses Draw:</p>
    <pre>{dumps(data.bonuses_draw, indent=json_indent)}</pre>
    """

def _build_bonuses_draw(data: Column) -> list[BonusDraw]:
    """Build bonuses draw"""
    bonuses_draw: list[BonusDraw] = []

    for value in data:
        bonus_draw_dict: Final[dict] = loads(value)
        bonuses_draw.append(BonusDraw(**bonus_draw_dict))

    return bonuses_draw