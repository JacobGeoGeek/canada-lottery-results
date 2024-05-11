"""create lottery tables

Revision ID: 6193c89488ba
Revises: 
Create Date: 2024-01-24 20:33:35.646800

"""
from typing import Final, Sequence, Union

from alembic import op
from requests import Response
import sqlalchemy as sa
from src.common.models.numbers_matched import NumbersMatched
from src.daily_grand.entities.daily_grand_results import DailyGrandResults
from src.daily_grand.models.prize_breakdown import PrizeBreakdown
from src.daily_grand.models.result import Result as DailyGrandResult
from src.six_fourty_nine.models.result import Result as SixFourtyNineResult
from src.lottomax.models.prize_breakdown import PrizeBreakdown as LottomaxPrizeBreakdown
from src.six_fourty_nine.models.prize_breakdown import PrizeBreakdown as SixFourtyNinePrizeBreakdown

from src.lottomax.entities.lotto_max_results import LottoMaxResults
from src.daily_grand.entities.daily_grand_results import DailyGrandResults
from src.six_fourty_nine.entities.six_fourty_nine_results import SixFourtyNineResults

from src.lottomax import lottomax_external_data
from src.lottomax.models.region import Region
from src.six_fourty_nine import six_fourty_nine_external_data
from src.daily_grand import daily_grand_external_data
from src.games.entities.games import Games
from src.lottomax.models.numbers import Numbers

# revision identifiers, used by Alembic.
revision: str = '6193c89488ba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def _create_lottery_tables() -> None:
    print("Creating tables")
    op.create_table("games",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String, unique=True, nullable=False),
        sa.Column("years", sa.ARRAY(sa.Integer), nullable=False)
    )
    op.create_table("lotto_max_draw_results",
        sa.Column("date", sa.Date, nullable=False, primary_key=True),
        sa.Column("game_id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("numbers", sa.ARRAY(sa.Integer), nullable=False),
        sa.Column("bonus", sa.Integer, nullable=False),
        sa.Column("prize", sa.Float, nullable=False),
        sa.Column("summary", sa.JSON, nullable=False),
        sa.Column("numbers_matched", sa.JSON, nullable=False),
        sa.Column("numbers_matched_atlantic", sa.JSON, nullable=False),
        sa.Column("numbers_matched_british_columbia", sa.JSON, nullable=False),
        sa.Column("numbers_matched_ontario", sa.JSON, nullable=False),
        sa.Column("numbers_matched_quebec", sa.JSON, nullable=False),
        sa.Column("numbers_matched_western_canada", sa.JSON, nullable=False),
        sa.UniqueConstraint("date", "game_id")
    )
    op.create_table("daily_grand_draw_results",
        sa.Column("date", sa.Date, nullable=False, primary_key=True),
        sa.Column("game_id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("numbers", sa.ARRAY(sa.Integer), nullable=False),
        sa.Column("grand_number", sa.Integer, nullable=False),
        sa.Column("bonuses_draw", sa.JSON, nullable=True),
        sa.Column("prize", sa.Float, nullable=False),
        sa.Column("main_breakdown", sa.JSON, nullable=False),
        sa.Column("bonus_breakdown", sa.JSON, nullable=False),
        sa.UniqueConstraint("date", "game_id")
    )
    op.create_table("six_fourty_nine_draw_results",
        sa.Column("date", sa.Date, nullable=False, primary_key=True),
        sa.Column("game_id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("classic", sa.JSON, nullable=False),
        sa.Column("guaranteed", sa.JSON, nullable=True),
        sa.Column("gold_ball", sa.JSON, nullable=True),
        sa.Column("summary", sa.JSON, nullable=False),
        sa.Column("number_matched", sa.JSON, nullable=False),
        sa.UniqueConstraint("date", "game_id")
    )

def _drop_lottery_tables() -> None:
    op.drop_table("games")
    op.drop_table("lotto_max_draw_results")
    op.drop_table("daily_grand_draw_results")
    op.drop_table("six_fourty_nine_draw_results")

def _populate_game_table(lotto_max_id: int, daily_grand_id: int, six_fourty_nine_id: int, lotto_max_years: list[int], daily_grand_years: list[int], six_fourty_nine_years: list[int]) -> None:
    print("Populating game table")
    op.bulk_insert(
        Games.__table__,
        [
            {"id": lotto_max_id, "name": "lottomax", "years": lotto_max_years},
            {"id": daily_grand_id, "name": "dailygrand", "years": daily_grand_years},
            {"id": six_fourty_nine_id, "name": "sixfourtynine", "years": six_fourty_nine_years},
        ]
    )

def _populate_lotto_max_table(id: int, years: list[int]) -> None:
    print("Populating lottomax table")
    insert_values_lotto_max = []
    
    for year in years:
      print(f"Populating lottomax table for year {year}")
      number_results: Final[list[Numbers]] = lottomax_external_data.extract_lotto_numbers_by_year(year)
      for result in number_results:
        print(f"Populating lottomax table for date {result.date}")
       
        prize: LottomaxPrizeBreakdown = lottomax_external_data.extract_lotto_result(result.date)
        number_matched: list[str] = list(map(lambda match: match.model_dump_json(), prize.numbers_matched))

        detail_result_ontario: list[NumbersMatched] = lottomax_external_data.extract_lotto_result_by_date_and_region(result.date, Region.ONTARIO)
        detail_result_ontario: list[str] = list(map(lambda match: match.model_dump_json(), detail_result_ontario))

        detail_result_quebec: list[NumbersMatched] = lottomax_external_data.extract_lotto_result_by_date_and_region(result.date, Region.QUEBEC)
        detail_result_quebec: list[str] = list(map(lambda match: match.model_dump_json(), detail_result_quebec))
    
        detail_result_western: list[NumbersMatched] = lottomax_external_data.extract_lotto_result_by_date_and_region(result.date, Region.WESTERN_CANADA)
        detail_result_western: list[str] = list(map(lambda match: match.model_dump_json(), detail_result_western))
    
        detail_result_atlantic: list[NumbersMatched] = lottomax_external_data.extract_lotto_result_by_date_and_region(result.date, Region.ATLANTIC)
        detail_result_atlantic: list[str] = list(map(lambda match: match.model_dump_json(), detail_result_atlantic))
    
        detail_result_british: list[NumbersMatched] = lottomax_external_data.extract_lotto_result_by_date_and_region(result.date, Region.BRITISH_COLUMBIA)
        detail_result_british: list[str] = list(map(lambda match: match.model_dump_json(), detail_result_british))

        insert_values_lotto_max.append({
            "date": result.date,
            "game_id": id,
            "numbers": result.numbers,
            "bonus": result.bonus,
            "prize": result.prize,
            "summary": prize.summary.model_dump_json(),
            "numbers_matched": number_matched,
            "numbers_matched_atlantic": detail_result_atlantic,
            "numbers_matched_british_columbia": detail_result_british,
            "numbers_matched_ontario": detail_result_ontario,
            "numbers_matched_quebec": detail_result_quebec,
            "numbers_matched_western_canada": detail_result_western
            })
    
    op.bulk_insert(LottoMaxResults.__table__, insert_values_lotto_max)
        
def _populate_daily_grand_table(id: int, years: list[int]) -> None:
    print("Populating daily grand table")
    insert_values = []

    for year in years:
     print(f"Populating daily grand table for year {year}")
     results: list[DailyGrandResult] = daily_grand_external_data.extract_daily_grand_results(year)

     for result in results:
        print(f"Populating daily grand table for date {result.date}")
        response_data: Final[Response] = daily_grand_external_data.fetch_daily_grand_result(result.date)
        winners: PrizeBreakdown = daily_grand_external_data.extract_daily_grand_prize_breakdown(response_data)
        insert_values.append({
            "date": result.date,
            "game_id": id,
            "numbers": result.numbers,
            "grand_number": result.grand_number,
            "bonuses_draw": list(map(lambda draw: draw.model_dump_json(), result.bonuses_draw)),
            "prize": result.prize,
            "main_breakdown": winners.main_breakdown.model_dump_json(),
            "bonus_breakdown": winners.bonuses_breakdown.model_dump_json() if winners.bonuses_breakdown else None
        })
    
    op.bulk_insert(DailyGrandResults.__table__, insert_values)

def _populate_six_fourty_nine_table(id: int, years: list[int]) -> None:
    print("Populating six fourty nine table")
    insert_values = []

    for year in years:
      print(f"Populating six fourty nine table for year {year}")
      results: list[SixFourtyNineResult] = six_fourty_nine_external_data.extract_649_results(year)

      for result in results:
        print(f"Populating six fourty nine table for date {result.date}")
        details: Final[SixFourtyNinePrizeBreakdown | None] = six_fourty_nine_external_data.extract_649_prize_breakdown(result.date)
        insert_values.append({
            "date": result.date,
            "game_id": id,
            "classic": result.classic.model_dump_json(),
            "guaranteed": list(map(lambda guaranteed: guaranteed.model_dump_json(), result.guaranteed)) if result.guaranteed else None,
            "gold_ball": result.gold_ball.model_dump_json() if result.gold_ball else None,
            "summary": details.summary.model_dump_json() if details else None,
            "number_matched": list(map(lambda match: match.model_dump_json(), details.numbers_matched)) if details else None
        })

    op.bulk_insert(SixFourtyNineResults.__table__, insert_values)
    
def _populate_tables() -> None:
    lotto_max_id: Final[int] = 1
    daily_grand_id: Final[int] = 2
    six_fourty_nine_id: Final[int] = 3
    lotto_max_years: Final[list[int]] = lottomax_external_data.extract_all_years()
    daily_grand_years: Final[list[int]] = daily_grand_external_data.extract_all_years()
    six_fourty_nine_years: Final[list[int]] = six_fourty_nine_external_data.extract_all_years()

    _populate_game_table(lotto_max_id, daily_grand_id, six_fourty_nine_id, lotto_max_years, daily_grand_years, six_fourty_nine_years)
    _populate_lotto_max_table(lotto_max_id, lotto_max_years)
    _populate_daily_grand_table(daily_grand_id, daily_grand_years)
    _populate_six_fourty_nine_table(six_fourty_nine_id, six_fourty_nine_years)

def upgrade() -> None:
    _create_lottery_tables()
    _populate_tables()

def downgrade() -> None:
    _drop_lottery_tables()