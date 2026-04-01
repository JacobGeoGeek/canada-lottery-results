from sqlalchemy import ARRAY, JSON, Column, Date, Float, Integer
from sqlalchemy.orm import declarative_base


## # Model represent prize statistic
# {
#   "date": "2023-10-01",
#   "gameId": 1,
#  "numbers": [1, 2, 3, 4, 5]
#    "bonus": 6,
#   "prize": 1000000,
#   "main_breakdown": {
#    "summary": {
#           "total_winners": -1,
#           "prize_fund": -1
#       },
#    "numbers_matched": [
#       {
#         "match": "",
#         "prize_per_winner": -1,
#         "total_winners": -1,
#         "prize_fund": -1
#       }
#     ]}
#   "OneMillionJackPotBreakdown": [
#     {
#       "number": [],
#       "prize_per_winner": -1,
#       "total_winners": -1,
#       "prize_fund": -1
#     }
#   ],
Base = declarative_base()
class WesternMaxResults(Base):
    __tablename__ = "western_max_draw_results"
    date: Column = Column(Date, primary_key=True, nullable=False)
    game_id: Column = Column(Integer, primary_key=True, nullable=False)
    numbers: Column = Column(ARRAY(Integer), nullable=False)
    bonus: Column = Column(Integer, nullable=False)
    prize: Column = Column(Float, nullable=False)
    main_breakdown: Column = Column(JSON, nullable=False)
    one_million_jackpot_breakdown: Column = Column(JSON, nullable=False)
