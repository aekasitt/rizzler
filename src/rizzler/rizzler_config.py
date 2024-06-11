#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/rizzler_config.py
# VERSION:     0.1.5
# CREATED:     2024-06-05 01:43
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module containing `RizzlerConfig` class"""

### Standard packages ###
from typing import Callable, List, Tuple

### Third-party packages ###
from pydantic import ValidationError

### Local modules ###
from rizzler.load_config import LoadConfig


class RizzlerConfig(object):
  _command: str = "pnpm"
  _framework: str = "vue"
  _logger_name: str = "uvicorn"

  @classmethod
  def load_config(cls, settings: Callable[..., List[Tuple]]) -> None:
    """
    Loads the Configuration from a Pydantic "BaseSettings" object or a List of parameter tuples.
    If not specified otherwise, each item should be provided as a string.

    ---
    """
    try:
      config = LoadConfig(**{key.lower(): value for key, value in settings()})
      cls._command = config.command or cls._command
      cls._framework = config.framework or cls._framework
      cls._logger_name = config.logger_name or cls._logger_name
    except ValidationError:
      raise
    except Exception:
      raise TypeError('RizzlerConfig must be pydantic "BaseSettings" or list of tuples')


__all__ = ("RizzlerConfig",)
