import datetime 
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from nba_scraper.db.base import Base

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, repr=True)
    abbreviation: Mapped[str] = mapped_column(String(3), unique=True, repr=True)
    city: Mapped[str] = mapped_column(repr=True)
    name: Mapped[str] = mapped_column(repr=True)

class Game(Base):
    __tablename__ = "games"

    id: Mapped[str] = mapped_column(primary_key=True, repr=True)
    date: Mapped[datetime.date] = mapped_column(repr=True)
    home_team_id: Mapped[int] = mapped_column(repr=True)
    away_team_id: Mapped[int] = mapped_column(repr=True)
    home_score: Mapped[int] = mapped_column(repr=True)
    away_score: Mapped[int] = mapped_column(repr=True)
    winner: Mapped[int] = mapped_column(repr=True)

class Player(Base):
    __tablename__ = "players"

    id: Mapped[str] = mapped_column(primary_key=True, repr=True)
    first_name: Mapped[str] = mapped_column(repr=True)
    last_name: Mapped[str] = mapped_column(repr=True)
    position: Mapped[str] = mapped_column(repr=True)
    height: Mapped[int] = mapped_column(repr=True)
    date_of_birth: Mapped[datetime.date] = mapped_column(repr=True)
    is_active: Mapped[bool] = mapped_column(repr=True)

class PlayerStats(Base):
    __tablename__ = "player_stats"

    player_id: Mapped[str] = mapped_column(primary_key=True, repr=True)
    game_id: Mapped[str] = mapped_column(primary_key=True, repr=True)
    team_id: Mapped[int] = mapped_column(repr=True)
    minutes: Mapped[int] = mapped_column(repr=True)
    field_goals_made: Mapped[int] = mapped_column(repr=True)
    field_goals_attempted: Mapped[int] = mapped_column(repr=True)
    field_goals_percentage: Mapped[int] = mapped_column(repr=True)
    three_pointers_made: Mapped[int] = mapped_column(repr=True)
    three_pointers_attempted: Mapped[int] = mapped_column(repr=True)
    three_pointers_percentage: Mapped[int] = mapped_column(repr=True)
    free_throws_made: Mapped[int] = mapped_column(repr=True)
    free_throws_attempted: Mapped[int] = mapped_column(repr=True)
    free_throws_percentage: Mapped[int] = mapped_column(repr=True)
    rebounds_offensive: Mapped[int] = mapped_column(repr=True)
    rebounds_defensive: Mapped[int] = mapped_column(repr=True)
    rebounds_total: Mapped[int] = mapped_column(repr=True)
    assists: Mapped[int] = mapped_column(repr=True)
    steals: Mapped[int] = mapped_column(repr=True)
    blocks: Mapped[int] = mapped_column(repr=True)
    turnovers: Mapped[int] = mapped_column(repr=True)
    fouls_personal: Mapped[int] = mapped_column(repr=True)
    points: Mapped[int] = mapped_column(repr=True)
    plus_minus_points: Mapped[int] = mapped_column(repr=True)