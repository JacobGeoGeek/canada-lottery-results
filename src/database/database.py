from contextlib import contextmanager
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.config.configuration import configuration

class Database:
    def __init__(self, connection_string: str) -> None:
        print(f"Database connection string: {connection_string}")
        self.engine: Engine = create_engine(connection_string)
        self.SessionLocal: Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextmanager
    def get_db(self) -> Session:
        try:
            yield self.SessionLocal()
        finally:
            self.SessionLocal().close()

database = Database(configuration.database_connection_string)