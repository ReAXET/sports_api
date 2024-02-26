"""Custom path configuration for the application."""

from __future__ import annotations

import os
from pathlib import Path

REPO_DIR = Path(__file__).parents[3]

APP_DIR = Path(__file__).parents[1]

LOG_DIR = Path(APP_DIR, 'logs')
# Check if the logs directory exists
if not LOG_DIR.is_dir():
    os.makedirs(LOG_DIR)

DATA_DIR = Path(APP_DIR, 'data')

RESOURCE_DIR = Path(APP_DIR, 'resources')

STATIC_DIR = Path(APP_DIR, 'static')

TEMPLATES_DIR = Path(APP_DIR, 'templates')
