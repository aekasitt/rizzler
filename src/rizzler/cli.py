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

### Standard packages ###
from typing import Dict, List, Tuple

### Third-party packages ###
from click import command, option
from rich import print

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
def rzl(
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
  """Command line entry point for `rzl`"""

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
  def rizzler_settings() -> List[Tuple[str, str]]:
    return [("command", command), ("framework", framework)]

  print(Rizzler._command, Rizzler._framework)


__all__ = ("rzl",)
