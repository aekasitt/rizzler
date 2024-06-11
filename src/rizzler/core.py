#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/core.py
# VERSION:     0.1.5
# CREATED:     2024-06-05 01:43
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module containing Core implementation for Rizzler extension for ASGI Frameworks"""

### Standard packages ###
from asyncio import create_subprocess_shell, ensure_future, gather
from asyncio.streams import StreamReader
from asyncio.subprocess import PIPE, Process
from logging import Logger, getLogger
from typing import Tuple

### Local modules ###
from rizzler.rizzler_config import RizzlerConfig


async def log_stderr(logger: Logger, stream: None | StreamReader) -> None:
  if stream is not None:
    while chunk := await stream.readline():
      logger.error(f"{chunk.decode('utf-8').strip()}")


async def log_stdout(logger: Logger, stream: None | StreamReader) -> None:
  if stream is not None:
    while chunk := await stream.readline():
      logger.info(f"{chunk.decode('utf-8').strip()}")


class Rizzler(RizzlerConfig):
  _process: None | Process = None

  @classmethod
  async def build(cls) -> Tuple[int, None, None]:
    command: str = f"{ cls._command } run" if cls._command != "yarn" else "yarn"
    logger: Logger = getLogger(cls._logger_name)
    logger.info("⚡Building Rizzler front-end…")
    cls._process = await create_subprocess_shell(
      f"{ command } build", stdout=PIPE, stderr=PIPE, restore_signals=True
    )
    return await gather(
      cls._process.wait(),
      log_stdout(logger, cls._process.stdout),
      log_stderr(logger, cls._process.stderr),
    )

  @classmethod
  async def initiate(cls) -> Tuple[int, None, None]:
    logger: Logger = getLogger(cls._logger_name)
    logger.info("⚡Initiating Rizzler…")
    cls._process = await create_subprocess_shell(
      f"{ cls._command } create vite@latest rzl-tmp --template { cls._framework }",
      stdout=PIPE,
      stderr=PIPE,
      restore_signals=True,
    )
    return await gather(
      cls._process.wait(),
      log_stdout(logger, cls._process.stdout),
      log_stderr(logger, cls._process.stderr),
    )

  @classmethod
  async def serve(cls) -> Process:
    command: str = f"{ cls._command } run" if cls._command != "yarn" else "yarn"
    logger: Logger = getLogger(cls._logger_name)
    logger.info("⚡Serving Rizzler dev-server…")
    cls._process = await create_subprocess_shell(
      f"{ command } dev", stdout=PIPE, stderr=PIPE, restore_signals=True
    )
    ensure_future(
      gather(
        cls._process.wait(),
        log_stdout(logger, cls._process.stdout),
        log_stderr(logger, cls._process.stderr),
      )
    )
    return cls._process

  @classmethod
  def shutdown(cls) -> None:
    logger: Logger = getLogger(cls._logger_name)
    if cls._process:
      try:
        logger.info("⚡Gracefully shutting down Rizzler")
        cls._process.terminate()
      except ProcessLookupError:
        ...


__all__ = ("Rizzler",)
