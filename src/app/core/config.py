from __future__ import annotations

import importlib
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Final, Literal
from dotenv import load_dotenv
from litestar.data_extractors import RequestExtractorField, ResponseExtractorField
from litestar.config import app
from pydantic_core import ValidationError
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict






DEFAULT_MODULE_NAME: Final[str] = 'app'
BASE_DIR: Final = Path(__file__).parent.parent
print(BASE_DIR)