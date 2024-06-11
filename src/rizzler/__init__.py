#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/__init__.py
# VERSION:     0.1.5
# CREATED:     2024-06-05 01:43
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************
"""ASGI extension that provides Single-Page Application Frameworks built into templates"""

__version__ = "0.1.5"

### Third-party packages ###
from click import group

### Local modules ###
from rizzler.core import Rizzler
from rizzler.commands import build, clean, initiate
from rizzler.templating import RizzleTemplates


@group
def cli() -> None:
  """rzl"""


cli.add_command(build, "build")
cli.add_command(clean, "clean")
cli.add_command(initiate, "initiate")

__all__ = ("RizzleTemplates", "Rizzler", "cli")
