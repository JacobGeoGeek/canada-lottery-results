
import datetime
from sqlalchemy import extract
from src.database.database import database
from .entities.six_fourty_nine_results import SixFourtyNineResults


with database.get_db() as _database:
  def get_649_numbers_by_year(year: int) -> list[SixFourtyNineResults]:
    return _database.query(SixFourtyNineResults.date, SixFourtyNineResults.classic, SixFourtyNineResults.guaranteed, SixFourtyNineResults.gold_ball).filter(extract('year', SixFourtyNineResults.date) == year).all()

  def get_649_numbers_by_date(date: datetime.date) -> SixFourtyNineResults:
    return _database.query(SixFourtyNineResults.summary, SixFourtyNineResults.number_matched).filter(SixFourtyNineResults.date == date).first()