from sqlalchemy import JSON, Column, Date, Float, Integer, UniqueConstraint
from sqlalchemy.orm import declarative_base

#   "extraPrize": {
#     "number": -1,
#     "prize": 10000000,
#     "breakdown": [
#       {
#         "match": "",
#         "prize_per_winner": -1,
#         "total_winners": -1,
#         "prize_fund": -1
#       }
#     ]
#   }
# }
Base = declarative_base()
class ExtraResults(Base):
    __tablename__ = "wclc_extra_draw_results"
    
    date: Column = Column(Date, primary_key=True, nullable=False)
    game_id: Column = Column(Integer, primary_key=True, nullable=False)
    number: Column = Column(Integer, nullable=False)
    prize: Column = Column(Float, nullable=False)
    summary: Column = Column(JSON, nullable=False)
    number_matched: Column = Column(JSON, nullable=False)

    __table_args__ = (
        UniqueConstraint("date", "game_id")
    )