#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Custom Logger implementation for the application"""
from __future__ import annotations

import os

from typing import TYPE_CHECKING

from loguru import logger

from app.core.config import Settings
from app.core import path_config


if TYPE_CHECKING:
    import loguru


class SportsLogger:

    def __init__(self):
        self.log_path = path_config.LOG_DIR

    def log(self) -> loguru.Logger:
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

        log_stdout_file = os.path.join(self.log_path, "sports_db_stdout.log")
        log_stderr_file = os.path.join(self.log_path, "sports_db_stderr.log")

        log_config = dict(rotation="1 week",
                          retention="1 month",
                          compression="zip",
                          enqueue=True)
        logger.add(
            log_stdout_file,  # type: ignore
            level="INFO",
            filter=lambda record: record['level'].name == 'INFO' or record[
                'level'].no > 20,
            **log_config)  # type: ignore

        logger.add(
            log_stderr_file,  # type: ignore
            level="ERROR",
            filter=lambda record: record['level'].name == 'ERROR',
            **log_config,  # type: ignore
            backtrace=True,
            diagnose=True)

        return logger


sports_logger = SportsLogger().log()
