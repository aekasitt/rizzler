#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2024-2026, All rights reserved.
# FILENAME:    ~~/src/rizzler/configs.py
# VERSION:     0.2.0
# CREATED:     2024-06-11 19:26 +0700
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard library ###
from pathlib import Path
from typing import Any, Literal

### Third-party packages ###
from pydantic import TypeAdapter
from yaml import Loader, load


file_path: Path = Path(__file__).resolve()

SCRIPT: list[str]
with open(str(file_path).replace("configs.py", "script.yaml"), "rb") as stream:
    script: dict[str, Any] | None = load(stream, Loader=Loader)
    if script:
        SCRIPT = TypeAdapter(list[str]).validate_python(script["serve"])

TEMPLATES: dict[Literal["base", "react", "svelte", "vue"], dict[int, str]]
with open(str(file_path).replace("configs.py", "templates.yaml"), "rb") as stream:
    templates: dict[str, Any] | None = load(stream, Loader=Loader)
    if templates:
        TEMPLATES = TypeAdapter(
            dict[Literal["base", "react", "svelte", "vue"], dict[int, str]]
        ).validate_python(templates["templates"])

__all__: tuple[str, ...] = ("SCRIPT", "TEMPLATES")
