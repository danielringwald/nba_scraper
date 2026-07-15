from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from nba_scraper.db.base import Base

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, repr=True)
    abbreviation: Mapped[str] = mapped_column(String(3), unique=True, repr=True)
    city: Mapped[str] = mapped_column(repr=True)
    name: Mapped[str] = mapped_column(repr=True)