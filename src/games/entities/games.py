
from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Games(Base):
  __tablename__ = "games"

  id: Column = Column(Integer, primary_key=True, index=True)
  name: Column = Column(String, unique=True, nullable=False)
  years: Column = Column(ARRAY(Integer), nullable=False)