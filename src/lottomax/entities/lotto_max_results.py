from sqlalchemy import ARRAY, Column, Date, Float, Integer, JSON, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class LottoMaxResults(Base):
  __tablename__ = "lotto_max_draw_results"

  date: Column = Column(Date, primary_key=True, nullable=False)
  game_id: Column = Column(Integer, primary_key=True, nullable=False)
  numbers: Column = Column(ARRAY(Integer), nullable=False)
  bonus: Column = Column(Integer, nullable=False)
  prize: Column = Column(Float, nullable=False)
  summary: Column = Column(JSON, nullable=False)
  numbers_matched: Column = Column(JSON, nullable=False)
  numbers_matched_atlantic: Column = Column(JSON, nullable=False)
  numbers_matched_british_columbia: Column = Column(JSON, nullable=False)
  numbers_matched_ontario: Column = Column(JSON, nullable=False)
  numbers_matched_quebec: Column = Column(JSON, nullable=False)
  numbers_matched_western_canada: Column = Column(JSON, nullable=False)

  __table_args__ = (
    UniqueConstraint("date", "game_id"),
  )