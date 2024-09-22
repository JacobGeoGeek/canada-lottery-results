"""update_total_winners_lottomax

Revision ID: 0555d3d29f6e
Revises: 6193c89488ba
Create Date: 2024-09-17 16:00:55.927859

"""
import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.common.models.numbers_matched import NumbersMatched
from src.lottomax import lottomax_external_data
from src.lottomax.models.prize_breakdown import PrizeBreakdown
from src.lottomax.models.region import Region


# revision identifiers, used by Alembic.
revision: str = '0555d3d29f6e'
down_revision: Union[str, None] = '6193c89488ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection: sa.Connection = op.get_bind()
    results: Sequence[sa.Row] = connection.execute(sa.text("SELECT date FROM lotto_max_draw_results")).fetchall()
    
    for row in results:
        print(f"Updating total winners for {row.date}")
        prize: PrizeBreakdown = lottomax_external_data.extract_lotto_result(row.date)
        
        number_matched: list[dict] = list(map(lambda match: match.model_dump(mode="json"), prize.numbers_matched))
        
        detail_result_ontario: list[NumbersMatched] = lottomax_external_data.extract_lotto_result_by_date_and_region(row.date, Region.ONTARIO)
        detail_result_ontario: list[dict] = list(map(lambda match: match.model_dump(mode="json"), detail_result_ontario))

        detail_result_quebec: list[NumbersMatched] = lottomax_external_data.extract_lotto_result_by_date_and_region(row.date, Region.QUEBEC)
        detail_result_quebec: list[dict] = list(map(lambda match: match.model_dump(mode="json"), detail_result_quebec))
    
        detail_result_western: list[NumbersMatched] = lottomax_external_data.extract_lotto_result_by_date_and_region(row.date, Region.WESTERN_CANADA)
        detail_result_western: list[dict] = list(map(lambda match: match.model_dump(mode="json"), detail_result_western))
    
        detail_result_atlantic: list[NumbersMatched] = lottomax_external_data.extract_lotto_result_by_date_and_region(row.date, Region.ATLANTIC)
        detail_result_atlantic: list[dict] = list(map(lambda match: match.model_dump(mode="json"), detail_result_atlantic))
    
        detail_result_british: list[NumbersMatched] = lottomax_external_data.extract_lotto_result_by_date_and_region(row.date, Region.BRITISH_COLUMBIA)
        detail_result_british: list[dict] = list(map(lambda match: match.model_dump(mode="json"), detail_result_british))

        connection.execute(
            sa.text("""
                UPDATE lotto_max_draw_results
                SET summary = :summary,
                    numbers_matched = :numbers_matched,
                    numbers_matched_atlantic = :numbers_matched_atlantic,
                    numbers_matched_british_columbia = :numbers_matched_british_columbia,
                    numbers_matched_ontario = :numbers_matched_ontario,
                    numbers_matched_quebec = :numbers_matched_quebec,
                    numbers_matched_western_canada = :numbers_matched_western_canada
                WHERE date = :date
            """),
                {
                    "summary": json.dumps(prize.summary.model_dump(mode="json")),
                    "numbers_matched": json.dumps(number_matched),
                    "numbers_matched_atlantic": json.dumps(detail_result_atlantic),
                    "numbers_matched_british_columbia": json.dumps(detail_result_british),
                    "numbers_matched_ontario": json.dumps(detail_result_ontario),
                    "numbers_matched_quebec": json.dumps(detail_result_quebec),
                    "numbers_matched_western_canada": json.dumps(detail_result_western),
                    "date": row.date
                }
            )

def downgrade() -> None:
    pass