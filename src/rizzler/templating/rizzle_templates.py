#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024, All rights reserved.
# FILENAME:    ~~/src/rizzler/templating/rizzle_template.py
# VERSION:     0.1.5
# CREATED:     2024-06-07 01:39
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List

### Third-party packages ###
from markupsafe import Markup
from starlette.templating import Jinja2Templates

### Local modules ###
from rizzler import Rizzler


class RizzleTemplates(Jinja2Templates):
  def __init__(self, directory: str) -> None:
    super().__init__(directory=directory)
    self.env.globals["vite_hmr_client"] = self.vite_hmr_client
    self.env.globals["vite_asset"] = self.vite_asset

  @classmethod
  def vite_asset(cls, path: str) -> Markup:
    tags: List[str] = []
    tags.append(
      """
      <script async defer type="module" src="http://localhost:5173/%s"></script>
      """
      % path
    )
    return Markup("\n".join(tags))

  @classmethod
  def vite_hmr_client(cls) -> Markup:
    """ """
    tags: List[str] = []
    tags.append(
      """
      <script type="module" src="http://localhost:5173/@vite/client"></script>
      """
    )
    if Rizzler._framework == "react":
      tags.append(
        """
        <script type="module">
          import RefreshRuntime from 'http://localhost:5173/@react-refresh'
          RefreshRuntime.injectIntoGlobalHook(window)
          window.$RefreshReg$ = () => {{}}
          window.$RefreshSig$ = () => (type) => type
          window.__vite_plugin_react_preamble_installed__=true
        </script>
        """
      )
    return Markup("\n".join(tags))


__all__ = ("RizzleTemplates",)
