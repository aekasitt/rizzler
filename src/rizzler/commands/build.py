#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/commands/build.py
# VERSION:     0.1.9
# CREATED:     2024-06-09 02:39
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from asyncio import run
from logging import Formatter, Logger, getLogger
from re import match, sub
from typing import Dict, List, Tuple

### Third-party packages ###
from click import command, option
from rich.logging import RichHandler
from tree_sitter import Language, Parser
from tree_sitter_html import language

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

  ### Tailor dist/index.html to be entry point ###
  html: Language = Language(language())
  parser: Parser = Parser(html)
  content: bytes
  overwrite: bytes = b""
  with open("templates/index.html", "rb") as file:
    content = file.read()
  tree = parser.parse(content, encoding="utf8")
  root_node = tree.root_node
  doctype_node = next(filter(lambda node: node.type == "doctype", root_node.children))
  overwrite += content[doctype_node.start_byte : doctype_node.end_byte]
  html_node = next(filter(lambda node: node.type == "element", root_node.children))
  cursor = html_node.walk()
  cursor.goto_first_child()
  while cursor.goto_next_sibling() and cursor.node is not None:
    if (
      match(r"^\<head\>", content[cursor.node.start_byte : cursor.node.end_byte].decode("utf8"))
      is not None
    ):
      head_tag: bytes = content[cursor.node.start_byte : cursor.node.end_byte]
      end_index: int = head_tag.decode("utf8").rindex(r"</head>")
      overwrite += content[cursor.node.start_byte : cursor.node.start_byte + end_index]
      overwrite += b'<link href="./rizz.css" rel="stylesheet">\n'
      overwrite += content[cursor.node.start_byte + end_index : cursor.node.end_byte]
    elif (
      match(r"^\<body\>", content[cursor.node.start_byte : cursor.node.end_byte].decode("utf8"))
      is not None
    ):
      body_tag: bytes = content[cursor.node.start_byte : cursor.node.end_byte]
      end_index: int = body_tag.decode("utf8").rindex(r"</body>")
      overwrite += content[cursor.node.start_byte : cursor.node.start_byte + end_index]
      overwrite += b'<script language="javascript" src="./rizz.js" type="module"></script>'
      overwrite += content[cursor.node.start_byte + end_index : cursor.node.end_byte]
  overwrite = sub(
    r"\{\{\s*vite_hmr_client\(\)\s*\}\}\n",
    "",
    overwrite.decode("utf8")
  ).encode("utf8")
  overwrite = sub(
    r"\{\{\s*vite_asset\((\"|')pages\/main\.js[x]?(\"|')\)\s*\}\}\n",
    "",
    overwrite.decode("utf8")
  ).encode("utf8")
  with open("dist/index.html", "wb") as file:
    file.write(overwrite)


__all__ = ("build",)
