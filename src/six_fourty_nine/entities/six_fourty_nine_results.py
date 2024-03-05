
from sqlalchemy import Column, Date, Integer, JSON, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SixFourtyNineResults(Base):
  __tablename__ = "six_fourty_nine_draw_results"

  date: Column = Column(Date, primary_key=True, nullable=False) 
  game_id: Column = Column(Integer, primary_key=True, nullable=False)
  classic: Column = Column(JSON, nullable=False)
  guaranteed: Column = Column(JSON, nullable=True)
  gold_ball: Column = Column(JSON, nullable=True)
  summary: Column = Column(JSON, nullable=False)
  number_matched: Column = Column(JSON, nullable=False)

  __table_args__ = (
    UniqueConstraint("date", "game_id"),
  )