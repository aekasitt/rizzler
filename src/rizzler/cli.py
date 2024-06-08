#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/cli.py
# VERSION:     0.1.3
# CREATED:     2024-06-08 00:05
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from click import group

### Local modules ###
from rizzler.commands import build, initiate


@group
def rzl() -> None:
  """Command line entry point for `rzl`"""


rzl.add_command(build, "build")
rzl.add_command(initiate, "init")


__all__ = ("rzl",)
