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
from logging import Formatter, Logger, getLogger
from shutil import rmtree
from os import path, remove

### Third-party packages ###
from click import command
from rich.logging import RichHandler


@command
def clean() -> None:
  """Clean up generated files from JavaScript Runtime's package manager"""
  logger: Logger = getLogger("rzl")
  logger.setLevel("INFO")
  handler: RichHandler = RichHandler()
  handler.setFormatter(Formatter("%(message)s", datefmt="[%X]"))
  logger.addHandler(handler)
  if path.exists("node_modules"):
    logger.info(f"D node_modules")
    rmtree("node_modules")
  if path.exists("package.json"):
    logger.info(f"D package.json")
    remove("package.json")
  if path.exists("package-lock.json"):
    logger.info(f"D package-lock.json")
    remove("package-lock.json")
  if path.exists("pnpm-lock.yaml"):
    logger.info(f"D pnpm-lock.yaml")
    remove("pnpm-lock.yaml")
  if path.exists("vite.config.js"):
    logger.info(f"D vite.config.js")
    remove("vite.config.js")
  if path.exists("yarn.lock"):
    logger.info(f"D yarn.lock")
    remove("yarn.lock")


__all__ = ("clean",)
