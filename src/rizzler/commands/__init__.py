#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/commands/__init__.py
# VERSION:     0.1.5
# CREATED:     2024-06-09 02:39
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************

### Local modules ###
from rizzler.commands.build import build
from rizzler.commands.clean import clean
from rizzler.commands.initiate import initiate

__all__ = ("build", "clean", "initiate")
