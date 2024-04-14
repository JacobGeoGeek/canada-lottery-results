import datetime

from sqlalchemy import extract

from src.database.database import database
from .entities.daily_grand_results import DailyGrandResults

with database.get_db() as _database:
  def get_daily_grand_numbers_by_year(year: int) -> list[DailyGrandResults]:
    return _database.query(DailyGrandResults.date, DailyGrandResults.numbers, DailyGrandResults.grand_number, DailyGrandResults.bonuses_draw, DailyGrandResults.prize).filter(extract('year', DailyGrandResults.date) == year).all()
  
  def get_daily_grand_numbers_by_date(date: datetime.date) -> DailyGrandResults:
    return _database.query(DailyGrandResults.main_breakdown, DailyGrandResults.bonus_breakdown).filter(DailyGrandResults.date == date).first()
  
  def save_daily_grand_result(daily_grand_result: DailyGrandResults) -> None:
    _database.add(daily_grand_result)
    _database.commit()
    _database.refresh(daily_grand_result)