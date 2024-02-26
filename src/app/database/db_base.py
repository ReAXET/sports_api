from __future__ import annotations


import os
from typing import Any, Dict, List, Optional, Union, Final, Literal
from pydantic_core import ValidationError, core_schema, from_json, to_json
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict, BaseSettings
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from dotenv import dotenv_values

from loguru import logger

from app.core.config import Settings
from app.common.logger import sports_logger


# Set the logger up
sports_logger = sports_logger

# Set the logger level
sports_logger.level("INFO")


metadata = MetaData()


class SQLAlchemyBase(DeclarativeBase):
    """SQLAlchemy base class."""

    def __tablename__(self) -> str:
        """Return the table name."""
        return self.__name__.lower()

    def __repr__(self) -> str:
        """Return the string representation of the class."""
        return f"<{self.__class__.__name__}({self.__dict__})>"


class DatabaseSettings(BaseModel):
    """Database settings class."""

    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      arbitrary_types_allowed=True)

    DATABASE_URL: Optional[str | None] = os.getenv("DATABASE_URL")
    DATABASE_USER: Optional[str | None] = os.getenv("DATABASE_USER")
    DATABASE_PASS: Optional[str | None] = os.getenv("DATABASE_PASS")
    DATABASE_HOST: Optional[str | None] = os.getenv("DATABASE_HOST")
    DATABASE_PORT: Optional[str | None] = os.getenv("DATABASE_PORT")
    DATABASE_NAME: Optional[str | None] = os.getenv("DATABASE_NAME")


Base = declarative_base(cls=SQLAlchemyBase)


def db_connect(settings: DatabaseSettings) -> Any:
    """Connect to the database.

    Args:
    ______
    settings (DatabaseSettings): The database settings.

    Returns:
    _______
    Any: The database connection.
    """

    DATABASE_URL = settings.DATABASE_URL
    DATABASE_USER = settings.DATABASE_USER
    DATABASE_PASS = settings.DATABASE_PASS
    DATABASE_HOST = settings.DATABASE_HOST
    DATABASE_PORT = settings.DATABASE_PORT
    DATABASE_NAME = settings.DATABASE_NAME

    if DATABASE_URL is None:
        DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASS}@{
            DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
        logger.info(f"DATABASE_URL: {DATABASE_URL}")

    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        sports_logger.info("Database connection successful.")
    except Exception as e:
        sports_logger.error(f"Database connection failed: {e}")
        raise e

    return engine, connection


def create_tables(engine: Any, base: SQLAlchemyBase) -> None:
    """Create the database tables.

    Args:
    ______
    engine (Any): The database engine.
    base (SQLAlchemyBase): The base class for all the models in the application.
    """

    try:
        base.metadata.drop_all(engine, checkfirst=True)
        base.metadata.create_all(engine, checkfirst=True)
        sports_logger.info("Database tables created.")
    except Exception as e:
        sports_logger.error(f"Database tables creation failed: {e}")
        raise e


def db_session(engine: Any) -> Any:
    # sourcery skip: inline-immediately-returned-variable
    """Create a database session.

    Args:
    ______
    engine (Any): The database engine.

    Returns:
    _______
    Any: The database session.
    """

    Session = sessionmaker(bind=engine)
    session = Session()
    return session
