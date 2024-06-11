#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/commands/build.py
# VERSION:     0.1.5
# CREATED:     2024-06-09 02:39
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from asyncio import run
from logging import Formatter, Logger, getLogger
from typing import Dict, List, Tuple

### Third-party packages ###
from click import command, option
from rich.logging import RichHandler

### Local modules ###
from rizzler.core import Rizzler
from rizzler.types import MutexOption


@command
@option(
  "--bun", alternatives=["deno", "npm", "pnpm", "yarn"], cls=MutexOption, is_flag=True, type=bool
)
@option(
  "--deno", alternatives=["bun", "npm", "pnpm", "yarn"], cls=MutexOption, is_flag=True, type=bool
)
@option(
  "--npm", alternatives=["bun", "deno", "pnpm", "yarn"], cls=MutexOption, is_flag=True, type=bool
)
@option(
  "--pnpm", alternatives=["bun", "deno", "npm", "yarn"], cls=MutexOption, is_flag=True, type=bool
)
@option(
  "--yarn", alternatives=["bun", "deno", "npm", "pnpm"], cls=MutexOption, is_flag=True, type=bool
)
def build(bun: bool, deno: bool, npm: bool, pnpm: bool, yarn: bool) -> None:
  """Build project"""
  command_selector: Dict[str, bool] = {
    "bun": bun,
    "deno": deno,
    "npm": npm,
    "pnpm": pnpm,
    "yarn": yarn,
  }
  command: str
  try:
    command = next(filter(lambda value: value[1], command_selector.items()))[0]
  except StopIteration:
    command = "pnpm"

  @Rizzler.load_config
  def rizzler_settings() -> List[Tuple[str, str]]:  # type: ignore
    return [("command", command), ("logger_name", "rzl")]

  logger: Logger = getLogger("rzl")
  logger.setLevel("INFO")
  handler: RichHandler = RichHandler()
  handler.setFormatter(Formatter("%(message)s", datefmt="[%X]"))
  logger.addHandler(handler)
  run(Rizzler.build())


__all__ = ("build",)
