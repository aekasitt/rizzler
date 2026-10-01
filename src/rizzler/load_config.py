#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2024-2026, All rights reserved.
# FILENAME:    ~~/src/rizzler/load_config.py
# VERSION:     0.2.0
# CREATED:     2024-06-05 01:43 +0700
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module containing `LoadConfig` Pydantic model"""

### Standard library ###
from typing import Annotated, Literal

### Third-party packages ###
from pydantic import BaseModel, BeforeValidator


def validate_logger_name(value: str) -> str:
    if value.lower() not in {"_granian", "granian", "gunicorn", "uvicorn"}:
        raise ValueError(
            'The "logger_name" value must be one of "granian", "gunicorn", or "uvicorn".'
        )
    if value.lower() == "granian":
        return "_granian"
    return value


class LoadConfig(BaseModel):
    command: Literal["bun", "deno", "npm", "pnpm", "yarn"] | None = None
    framework: Literal["angular", "react", "svelte", "vue"] | None = None
    logger_name: Annotated[
        Literal["_granian", "gunicorn", "uvicorn"] | None,
        BeforeValidator(validate_logger_name),
    ] = None


__all__: tuple[str, ...] = ("LoadConfig",)
