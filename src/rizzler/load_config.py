#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/load_config.py
# VERSION:     0.0.1
# CREATED: 	   2024-06-05 01:43
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module containing `LoadConfig` Pydantic model"""

### Standard packages ###
from typing import Optional

### Third-party packages ###
from pydantic import BaseModel, validator, StrictStr


class LoadConfig(BaseModel):
  command: Optional[StrictStr] = None
  framework: Optional[StrictStr] = None

  @validator("command")
  def validate_command(cls, value: str) -> str:
    if value.lower() not in {"bun", "deno", "npm", "pnpm", "yarn"}:
      raise ValueError(
        'The "command" value must be one of "bun", "deno", "npm", "pnpm", or "yarn".'
      )
    return value.lower()

  @validator("framework")
  def validate_framework(cls, value: int) -> int:
    if value.lower() not in {"angular", "react", "svelte", "vue"}:
      raise ValueError(
        'The "framework" value must be one of "angular", "react", "svelte", or "vue".'
      )
    return value


__all__ = ("LoadConfig",)
