

import datetime
from sqlalchemy import extract
from src.database import database
from .entities.western_max_results import WesternMaxResults


with database.get_db() as _database:
    def get_western_max_numbers_by_year(year: int) -> list[WesternMaxResults]:
        return _database.query(WesternMaxResults.date, WesternMaxResults.numbers, WesternMaxResults.bonus, WesternMaxResults.prize).filter(extract("year", WesternMaxResults.date) == year).all()
    
    def get_western_max_numbers_by_date(date: datetime.date) -> WesternMaxResults:
        return _database.query(WesternMaxResults.main_breakdown, WesternMaxResults.max_million_breakdown).filter(WesternMaxResults.date == date).first()
    
    def save_western_max_result(western_max_result: WesternMaxResults) -> None:
        _database.add(western_max_result)
        _database.commit()
        _database.refresh(western_max_result)