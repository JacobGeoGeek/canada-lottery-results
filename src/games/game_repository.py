from src.database.database import database
from .entities.games import Games

with database.get_db() as _database:
    def get_years_by_name(name: str) -> list[int]:
        return _database.query(Games).filter(Games.name == name).first().years

    def get_all_lotto_games() -> list[str]:
        return _database.query(Games).all().name
    
    def is_year_exist_by_name(name: str, year: int) -> bool:
        return year in get_years_by_name(name)
    
    def save_new_year_by_name(name: str, year: int) -> None:
        game: Games = _database.query(Games).filter(Games.name == name).first()
        game.years.insert(0, year)
        _database.commit()
        _database.refresh(game)