from datetime import datetime
from sqlalchemy import extract
from src.database.database import database
from .entities.lotto_max_results import LottoMaxResults

with database.get_db() as _database:
  def get_lotto_numbers_by_year(year: int) -> list[LottoMaxResults]:
    return _database.query(LottoMaxResults.date, LottoMaxResults.prize, LottoMaxResults.numbers, LottoMaxResults.bonus).filter(extract('year', LottoMaxResults.date) == year).all()
  
  def get_lotto_numbers_by_date(date: datetime.date) -> LottoMaxResults:
    return _database.query(LottoMaxResults.summary, LottoMaxResults.numbers_matched).filter(LottoMaxResults.date == date).first()
  
  def get_regions_numbers_matched_by_date(date: datetime.date) -> LottoMaxResults:
    return _database.query(LottoMaxResults.numbers_matched_atlantic, LottoMaxResults.numbers_matched_british_columbia, LottoMaxResults.numbers_matched_ontario, LottoMaxResults.numbers_matched_quebec, LottoMaxResults.numbers_matched_western_canada).filter(LottoMaxResults.date == date).first()
  
  def save_lotto_max_result(lotto_max_result: LottoMaxResults) -> None:
    _database.add(lotto_max_result)
    _database.commit()
    _database.refresh(lotto_max_result)