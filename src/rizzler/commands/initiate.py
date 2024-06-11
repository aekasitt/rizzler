#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/commands/initiate.py
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
from os import path, mkdir, remove
from shutil import move, rmtree
from re import sub
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
    return [("command", command), ("framework", framework), ("logger_name", "rzl")]

  logger: Logger = getLogger("rzl")
  logger.setLevel("INFO")
  handler: RichHandler = RichHandler()
  handler.setFormatter(Formatter("%(message)s", datefmt="[%X]"))
  logger.addHandler(handler)
  if not path.exists("rzl-tmp"):
    mkdir("rzl-tmp")
  run(Rizzler.initiate())
  if path.exists("package.json"):
    remove("package.json")
  move("rzl-tmp/package.json", "package.json")
  if path.exists("vite.config.js"):
    remove("vite.config.js")
  move("rzl-tmp/vite.config.js", "vite.config.js")
  if path.exists("pages"):
    rmtree("pages")
  move("rzl-tmp/src", "pages")
  if path.exists("public"):
    rmtree("public")
  move("rzl-tmp/public", "public")
  rmtree("rzl-tmp")
  if path.exists("templates"):
    rmtree("templates")
  mkdir("templates")
  with open("templates/index.html", "wb") as index_html:
    index_html.write(
      sub(
        r"\n {8}",
        "\n",
        """<!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="UTF-8" />
            <meta httprime-equiv='X-UA-Compatible' content='IE=edge' />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>
              Unspoken Rizz
            </title>
            <link href='/favicon.ico' rel='shortcut icon' type='image/x-icon'>
          </head>
          <body>
            <noscript>
              This page requires JavaScript to work.
            </noscript>
            <div id="{app_id}"></div>
            {{{{ vite_hmr_client() }}}}
            {{{{ vite_asset('{entry}') }}}}
          </body>
        </html>
        """,
      )
      .format(
        app_id="app" if framework != "react" else "root",
        entry="pages/main.js" if framework != "react" else "pages/main.jsx",
      )
      .encode("utf-8")
    )
  if path.exists("serve.py"):
    remove("serve.py")
  with open("serve.py", "wb") as serve_py:
    serve_py.write(
      sub(
        r"\n {8}",
        "\n",
        """#!/usr/bin/env python3
        from contextlib import asynccontextmanager
        from fastapi import FastAPI
        from fastapi.requests import Request
        from fastapi.responses import HTMLResponse
        from fastapi.staticfiles import StaticFiles
        from rizzler import Rizzler, RizzleTemplates
        from typing import List, Tuple

        templates = RizzleTemplates(directory="templates")

        @Rizzler.load_config
        def rizzler_settings() -> List[Tuple[str, str]]:
          return [("framework", "react")]

        @asynccontextmanager
        async def lifespan(_: FastAPI):
          await Rizzler.serve()
          yield
          Rizzler.shutdown()

        app = FastAPI(lifespan=lifespan)

        @app.get("/", response_class=HTMLResponse)
        def index(request: Request) -> HTMLResponse:
          return templates.TemplateResponse("index.html", {"request": request})
        app.mount("/", StaticFiles(directory="public"), name="public")
       """,
      ).encode("utf-8")
    )


__all__ = ("initiate",)
