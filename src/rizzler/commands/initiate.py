#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/commands/initiate.py
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
from os import path, mkdir, remove
from re import match, sub
from shutil import move, rmtree
from typing import Dict, List, Tuple

### Third-party packages ###
from click import command, option
from rich.logging import RichHandler
from tree_sitter import Language, Parser
from tree_sitter_javascript import language

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


def rizzify_vite_config(framework: str) -> bool:
  javascript: Language = Language(language())
  parser: Parser = Parser(javascript)
  content: bytes
  overwrite: bytes = b""
  with open("vite.config.js", "rb") as file:
    content = file.read()
  tree = parser.parse(content, encoding="utf8")
  root_node = tree.root_node
  export_node = next(filter(lambda node: node.type == "export_statement", root_node.children))
  cursor = export_node.walk()
  cursor.goto_first_child()
  while cursor.goto_next_sibling() and cursor.node is not None:
    if (
      match(r"^defineConfig", content[cursor.node.start_byte : cursor.node.end_byte].decode("utf8"))
      is not None
    ):
      define_cursor = cursor.node.walk()
      define_cursor.goto_first_child()
      while define_cursor.goto_next_sibling() and define_cursor.node is not None:
        if content[define_cursor.node.start_byte : define_cursor.node.end_byte] != b"defineConfig":
          config_cursor = define_cursor.node.walk()
          config_cursor.goto_first_child()
          while config_cursor.goto_next_sibling() and config_cursor.node is not None:
            if (
              match(
                r"^{",
                content[config_cursor.node.start_byte : config_cursor.node.end_byte].decode("utf8"),
              )
              is not None
            ):
              fields_cursor = config_cursor.node.walk()
              fields_cursor.goto_first_child()
              while fields_cursor.goto_next_sibling() and fields_cursor.node is not None:
                if (
                  match(
                    r"^,",
                    content[fields_cursor.node.start_byte : fields_cursor.node.end_byte].decode(
                      "utf8"
                    ),
                  )
                  is not None
                ):
                  entry_extension: str = "jsx" if framework == "react" else "js"
                  overwrite = content[0 : fields_cursor.node.start_byte + 1]
                  overwrite += sub(
                    r"\n\s{18}",
                    "\n",
                    """
                    build: {
                      rollupOptions: {
                        input: './pages/main.%s',
                        output: {
                          assetFileNames: 'rizz.[ext]',
                          entryFileNames: 'rizz.js'
                        },
                      },
                    },"""
                    % entry_extension,
                  ).encode("utf8")
                  overwrite += content[fields_cursor.node.end_byte : len(content)]
  with open("vite.config.js", "wb") as file:
    file.write(overwrite)

  return True


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
  rizzified = rizzify_vite_config(framework)
  if rizzified:
    logger.info("'./vite.config.js' file has been rizzified.")
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
