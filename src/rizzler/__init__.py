#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/__init__.py
# VERSION:     0.1.3
# CREATED:     2024-06-05 01:43
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************
"""ASGI extension that provides Single-Page Application Frameworks built into templates"""

__version__ = "0.1.3"

from rizzler.core import Rizzler
from rizzler.templating import RizzleTemplates

__all__ = ("RizzleTemplates", "Rizzler")
