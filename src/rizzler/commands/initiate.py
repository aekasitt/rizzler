#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/commands/initiate.py
# VERSION:     0.1.6
# CREATED:     2024-06-09 02:39
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from asyncio import run
from logging import Formatter, Logger, getLogger
from os import path, mkdir, remove
from shutil import move, rmtree
from typing import Dict, List, Tuple

### Third-party packages ###
from click import command, option
from rich.logging import RichHandler

### Local modules ###
from rizzler.configs import SCRIPT, TEMPLATES
from rizzler.core import Rizzler
from rizzler.types import MutexOption

def remove_if_exists(target: str) -> bool:
  removed: bool = False
  if path.exists(target):
    if path.isdir(target):
      rmtree(target)
    else:
      remove(target)
    removed = True
  return removed

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
    return [("command", command), ("framework", framework), ("logger_name", "rzl")]

  logger: Logger = getLogger("rzl")
  logger.setLevel("INFO")
  handler: RichHandler = RichHandler()
  handler.setFormatter(Formatter("%(message)s", datefmt="[%X]"))
  logger.addHandler(handler)

  if not path.exists("rzl-tmp"):
    mkdir("rzl-tmp")
  run(Rizzler.initiate())
  removed: bool = remove_if_exists("package.json")
  move("rzl-tmp/package.json", "package.json")
  logger.info(f"'./package.json' file has been {'rewritten' if removed else 'written'}.")
  removed = remove_if_exists("vite.config.js")
  move("rzl-tmp/vite.config.js", "vite.config.js")
  logger.info(f"'./vite.config.js' file has been {'rewritten' if removed else 'written'}.")
  removed = remove_if_exists("pages")
  move("rzl-tmp/src", "pages")
  logger.info(f"'./pages' directory has been {'recreated' if removed else 'created'}.")
  removed = remove_if_exists("public")
  move("rzl-tmp/public", "public")
  logger.info(f"'./public' directory has been {'recreated' if removed else 'created'}.")
  rmtree("rzl-tmp")
  logger.info("Temporary directory 'rzl-tmp' has been removed.")
  removed = remove_if_exists("templates")
  mkdir("templates")
  with open("templates/index.html", "wb") as index_html:
    index_html.write("\n".join(TEMPLATES[framework]).encode("utf-8"))  # type: ignore
  logger.info(f"'./templates' directory has been {'recreated' if removed else 'created'}.")
  logger.info(f"'./templates/index.html' has been {'rewritten' if removed else 'written'}.")
  removed = remove_if_exists("serve.py")
  with open("serve.py", "wb") as serve_py:
    serve_py.write("\n".join(SCRIPT).encode("utf-8"))  # type: ignore
  logger.info(f"'./serve.py' file has been {'recreated' if removed else 'created'}.")


__all__ = ("initiate",)
