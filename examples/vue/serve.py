#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/examples/vue/serve.py
# VERSION:     0.1.3
# CREATED:     2024-06-07 01:39
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from contextlib import asynccontextmanager
from typing import AsyncIterator

### Third-party packages ###
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from rizzler import RizzleTemplates, Rizzler
from uvicorn import run


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
  await Rizzler.initiate()
  yield
  Rizzler.terminate()


app: FastAPI = FastAPI(lifespan=lifespan)
templates: RizzleTemplates = RizzleTemplates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
  return templates.TemplateResponse("index.html", {"request": request, "title": "Unspoken Vue"})


app.mount("/public", StaticFiles(directory="public"), name="public")

if __name__ == "__main__":
  try:
    run(app)
  except KeyboardInterrupt:
    ...
