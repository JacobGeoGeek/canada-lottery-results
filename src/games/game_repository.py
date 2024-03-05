from src.database.database import database
from .entities.games import Games

with database.get_db() as _database:
    def get_years_by_name(name: str) -> list[int]:
        return _database.query(Games).filter(Games.name == name).first().years

    def get_all_lotto_games() -> list[str]:
        return _database.query(Games).all().name