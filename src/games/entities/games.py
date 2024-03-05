
from sqlalchemy import Integer, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()

class Games(Base):
  __tablename__ = "games"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
  name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
  years: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)