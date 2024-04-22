import datetime
from json import loads, dumps
from typing import Final

from sqlalchemy import Column

from src.common.models.numbers_matched import NumbersMatched
from src.common.models.summary import Summary

from .models.gold_ball import GoldBall
from .models.guaranteed import Guaranteed
from .models.classic import Classic
from .models.result import Result
from .models.prize_breakdown import PrizeBreakdown

from .entities.six_fourty_nine_results import SixFourtyNineResults

def build_649_results(data: list[SixFourtyNineResults]) -> list[Result]:
  """Build 6/49 results"""
  results: list[Result] = []

  for value in data:
    date: datetime.date = value.date
    classic: Classic = Classic(**loads(value.classic))
    guaranteed: list[Guaranteed] | None = None
    gold_ball: GoldBall | None = None

    if value.guaranteed is not None:
      guaranteed = _build_guaranteed(value.guaranteed)
    
    if value.gold_ball is not None:
      gold_ball_dict: Final[dict] = loads(value.gold_ball)
      gold_ball = GoldBall(number=gold_ball_dict["number"], prize=gold_ball_dict["prize"], isGoldBallDrawn=gold_ball_dict["is_gold_ball_drawn"])

    results.append(Result(date=date, classic=classic, guaranteed=guaranteed, goldBall=gold_ball))

  return results

def build_649_prize_breakdown(data: SixFourtyNineResults) -> PrizeBreakdown:
    """Build 6/49 prize breakdown"""
    summary: Final[Summary] = _build_summary(data.summary)
    numbers_matched: Final[list[NumbersMatched]] = _build_match_numbers(data.number_matched)
    return PrizeBreakdown(summary=summary, numbers_matched=numbers_matched)

def build_649_new_result(number_result: Result, prize_breakdown: PrizeBreakdown) -> SixFourtyNineResults:
   return SixFourtyNineResults(
    date=number_result.date,
    game_id=3,
    classic=number_result.classic.model_dump_json(),
    guaranteed=list(map(lambda guaranteed: guaranteed.model_dump_json(), number_result.guaranteed)) if number_result.guaranteed else None,
    gold_ball=number_result.gold_ball.model_dump_json() if number_result.gold_ball else None,
    summary=prize_breakdown.summary.model_dump_json() if prize_breakdown.summary else None,
    number_matched=list(map(lambda number_matched: number_matched.model_dump_json(), prize_breakdown.numbers_matched)) if prize_breakdown.numbers_matched else None
  )

def build_649_body_email(data: SixFourtyNineResults) -> str:
    """Build 6/49 body email"""
    json_indent: Final[int] = 4
    return f"""
    <h1>6/49 Result</h1>
    <p>Date: {data.date}</p>
    <p>Classic:</p>
    <pre>{dumps(data.classic, indent=json_indent)}</pre>
    <p>Guaranteed:</p>
    <pre>{dumps(data.guaranteed, indent=json_indent)}</pre>
    <p>Gold Ball:</p>
    <pre>{dumps(data.gold_ball, indent=json_indent)}</pre>
    <p>Summary:</p>
    <pre>{dumps(data.summary, indent=json_indent)}</pre>
    <p>Numbers Matched:</p>
    <pre>{dumps(data.number_matched, indent=json_indent)}</pre>
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

def _build_guaranteed(guaranteed: Column) -> list[Guaranteed]:
    """Build guaranteed"""
    result: Final[list[Guaranteed]] = []
    for value in guaranteed:
        guaranteed_dict = loads(value)
        result.append(Guaranteed(**guaranteed_dict))
    return result