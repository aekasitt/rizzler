#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2024-2026, All rights reserved.
# FILENAME:    ~~/src/rizzler/templating/rizzle_template.py
# VERSION:     0.2.0
# CREATED:     2024-06-07 01:39 +0700
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

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
        tags: list[str] = []
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
        tags: list[str] = []
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


__all__: tuple[str, ...] = ("RizzleTemplates",)
