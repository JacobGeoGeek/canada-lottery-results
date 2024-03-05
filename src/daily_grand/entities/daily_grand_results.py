from sqlalchemy import Column, Date, Float, Integer, JSON, ARRAY, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DailyGrandResults(Base):
  __tablename__ = "daily_grand_draw_results"

  date: Column = Column(Date, primary_key=True, nullable=False)
  game_id: Column = Column(Integer, primary_key=True, nullable=False)
  numbers: Column = Column(ARRAY(Integer), nullable=False)
  grand_number: Column = Column(Integer, nullable=False)
  bonuses_draw: Column = Column(JSON, nullable=True)
  prize: Column = Column(Float, nullable=False)
  main_breakdown: Column = Column(JSON, nullable=False)
  bonus_breakdown: Column = Column(JSON, nullable=False)

  __table_args__ = (
    UniqueConstraint("date", "game_id"),
  )