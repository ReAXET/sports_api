from __future__ import annotations

import importlib
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Final, Literal

from dotenv import load_dotenv
from litestar.config import app
from litestar.data_extractors import (RequestExtractorField,
                                      ResponseExtractorField)
from pydantic import field_validator
from pydantic_core import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from loguru import logger
from app.core import path_config


DEFAULT_MODULE_NAME: Final[str] = 'app'
APP_DIR: Final[Path] = path_config.APP_DIR
LOG_DIR: Final[Path] = path_config.LOG_DIR
DATA_DIR: Final[Path] = path_config.DATA_DIR
RESOURCE_DIR: Final[Path] = path_config.RESOURCE_DIR


# version from module pyproject.toml
VERSION: Final = importlib.import_module(
    f'{DEFAULT_MODULE_NAME}.__version__').__version__


__all__ = ["Settings", "app"]

# Load environment variables from .env file
load_dotenv()
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")


class Settings(BaseSettings):
    """Base settings class."""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_prefix='APP_',
        case_sensitive=False,
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )

    BUILD_NUMBER: str = ""
    DEBUG: bool = False
    ENVIRONMENT: Literal['development', 'production'] = 'development'
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR',
                       'CRITICAL'] = 'INFO'
    LOG_FILE: str = f"{APP_DIR}/logs/app.log"
    API_PREFIX: str = "/api/v1"
    API_TITLE: str = "Sports_DB API"
    API_DESCRIPTION: str = "API for sports database"
    API_VERSION: str = VERSION
    API_OPENAPI_URL: str = "/openapi.json"
    API_DOCS_URL: str = "/docs"
    API_REDOC_URL: str = "/redoc"
    API_SWAGGER_URL: str = "/swagger"
    API_SWAGGER_UI_OAUTH2_REDIRECT_URL: str = "/swagger/oauth2-redirect"
    API_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
