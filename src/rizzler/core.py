#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/core.py
# VERSION:     0.0.1
# CREATED:     2024-06-05 01:43
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module containing Core implementation for Rizzler extension for FastAPI"""

### Local modules ###
from rizzler.rizzler_config import RizzlerConfig


class Rizzler(RizzlerConfig): ...


__all__ = ("Rizzler",)
