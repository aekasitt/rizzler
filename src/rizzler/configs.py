#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/configs.py
# VERSION:     0.1.9
# CREATED:     2024-06-11 19:26
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

### Third-party packages ###
from pydantic import TypeAdapter
from yaml import Loader, load


file_path: Path = Path(__file__).resolve()

SCRIPT: List[str]
with open(str(file_path).replace("configs.py", "script.yaml"), "rb") as stream:
  script: Optional[Dict[str, Any]] = load(stream, Loader=Loader)
  if script:
    SCRIPT = TypeAdapter(List[str]).validate_python(script["serve"])

TEMPLATES: Dict[Literal["react", "vue"], List[str]]
with open(str(file_path).replace("configs.py", "templates.yaml"), "rb") as stream:
  templates: Optional[Dict[str, Any]] = load(stream, Loader=Loader)
  if templates:
    TEMPLATES = TypeAdapter(Dict[Literal["react", "vue"], List[str]]).validate_python(
      templates["templates"]
    )

__all__ = ("SCRIPT", "TEMPLATES")
