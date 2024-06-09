#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/commands/initiate.py
# VERSION:     0.1.4
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
  "--angular", alternatives=["react", "svelte", "vue"], cls=MutexOption, is_flag=True, type=bool
)
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
  "--react", alternatives=["angular", "svelte", "vue"], cls=MutexOption, is_flag=True, type=bool
)
@option(
  "--svelte", alternatives=["angular", "react", "vue"], cls=MutexOption, is_flag=True, type=bool
)
@option(
  "--vue", alternatives=["angular", "react", "svelte"], cls=MutexOption, is_flag=True, type=bool
)
@option(
  "--yarn", alternatives=["bun", "deno", "npm", "pnpm"], cls=MutexOption, is_flag=True, type=bool
)
def initiate(
  angular: bool,
  bun: bool,
  deno: bool,
  npm: bool,
  pnpm: bool,
  react: bool,
  svelte: bool,
  vue: bool,
  yarn: bool,
) -> None:
  """Initiate a new project"""
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

  framework_selector: Dict[str, bool] = {
    "angular": angular,
    "react": react,
    "svelte": svelte,
    "vue": vue,
  }
  framework: str
  try:
    framework = next(filter(lambda value: value[1], framework_selector.items()))[0]
  except StopIteration:
    framework = "vue"

  @Rizzler.load_config
  def rizzler_settings() -> List[Tuple[str, str]]:  # type: ignore
    return [("command", command), ("framework", framework), ("logger_name", "rizzler_cli")]

  logger: Logger = getLogger("rizzler_cli")
  logger.setLevel("INFO")
  handler: RichHandler = RichHandler()
  handler.setFormatter(Formatter("%(message)s", datefmt="[%X]"))
  logger.addHandler(handler)
  run(Rizzler.initiate())


__all__ = ("initiate",)
