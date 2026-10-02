#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2024-2026, All rights reserved.
# FILENAME:    ~~/src/rizzler/templating/minijinja.py
# VERSION:     0.2.1
# CREATED:     2026-10-01 17:36:35 +0700
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: Imitates starlette.templating._TemplateResponse and
#              starlette.templating.TemplateResponses using MiniJinja
# HISTORY:
# *************************************************************

### Standard packages ###
from collections.abc import Callable, Mapping, Sequence
from os import PathLike
from textwrap import dedent
from typing import Any
from warnings import warn

### Third-party packages ###
from markupsafe import Markup
from minijinja import Environment, load_from_path, pass_state
from starlette.responses import HTMLResponse

### Local modules ###
from rizzler.core import Rizzler


class _TemplateResponse(HTMLResponse):
    def __init__(
        self,
        env: Environment,
        name: str,
        context: dict[str, Any],
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: Any = None,
    ) -> None:
        self.template = name
        self.context = context
        super().__init__(
            env.render_template(name, **context),
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        request = self.context.get("request")
        extensions = request.get("extensions", {}) if request is not None else {}
        if "http.response.debug" in extensions:
            await send(
                {
                    "type": "http.response.debug",
                    "info": {
                        "template": self.template,
                        "context": self.context,
                    },
                }
            )
        await super().__call__(scope, receive, send)


class RizzleTemplates:
    """Render Rizzler templates with MiniJinja."""

    def __init__(
        self,
        directory: str | PathLike[str] | Sequence[str | PathLike[str]] | None = None,
        *,
        context_processors: list[Callable[[Any], dict[str, Any]]] | None = None,
        env: Environment | None = None,
        **env_options: Any,
    ) -> None:
        if (directory is None) == (env is None):
            raise ValueError("either 'directory' or 'env' must be passed")

        self.context_processors = context_processors or []
        if env is None:
            env_options.setdefault("loader", load_from_path(directory))
            env_options.setdefault("auto_escape_callback", lambda _: True)
            env = Environment(**env_options)
        elif env_options:
            raise TypeError("environment options cannot be used with 'env'")

        self.env = env
        self._setup_env_defaults()

    def _setup_env_defaults(self) -> None:
        @pass_state
        def url_for(state: Any, name: str, **path_params: Any) -> Markup:
            request = state.lookup("request")
            return Markup(str(request.url_for(name, **path_params)))

        defaults: dict[str, Any] = {
            "url_for": url_for,
            "vite_hmr_client": self.vite_hmr_client,
            "vite_asset": self.vite_asset,
        }
        globals_ = self.env.globals
        for name, value in defaults.items():
            if name not in globals_:
                self.env.add_global(name, value)

    def TemplateResponse(self, *args: Any, **kwargs: Any) -> _TemplateResponse:
        """Render a template using Starlette's TemplateResponse conventions."""
        if args and isinstance(args[0], str):
            warn(
                "The first TemplateResponse parameter should be the request. "
                "Use TemplateResponse(request, name, context).",
                DeprecationWarning,
                stacklevel=2,
            )
            name = args[0]
            context = args[1] if len(args) > 1 else kwargs.get("context")
            status_code = args[2] if len(args) > 2 else kwargs.get("status_code", 200)
            headers = args[3] if len(args) > 3 else kwargs.get("headers")
            media_type = args[4] if len(args) > 4 else kwargs.get("media_type")
            background = args[5] if len(args) > 5 else kwargs.get("background")
            context = {} if context is None else dict(context)
            if "request" not in context:
                raise ValueError('context must include a "request" key')
            request = context["request"]
        elif args:
            request = args[0]
            name = args[1] if len(args) > 1 else kwargs["name"]
            context = args[2] if len(args) > 2 else kwargs.get("context")
            status_code = args[3] if len(args) > 3 else kwargs.get("status_code", 200)
            headers = args[4] if len(args) > 4 else kwargs.get("headers")
            media_type = args[5] if len(args) > 5 else kwargs.get("media_type")
            background = args[6] if len(args) > 6 else kwargs.get("background")
            context = {} if context is None else dict(context)
        else:
            context = kwargs.get("context")
            context = {} if context is None else dict(context)
            request = kwargs.get("request", context.get("request"))
            if request is None:
                raise ValueError("TemplateResponse requires a request")
            name = kwargs["name"]
            status_code = kwargs.get("status_code", 200)
            headers = kwargs.get("headers")
            media_type = kwargs.get("media_type")
            background = kwargs.get("background")

        context.setdefault("request", request)
        for context_processor in self.context_processors:
            context.update(context_processor(request))

        return _TemplateResponse(
            self.env,
            name,
            context,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    @classmethod
    def vite_asset(cls, path: str) -> Markup:
        return Markup(
            dedent(
                """
                <script async defer type="module" src="http://localhost:5173/%s"></script>
                """
                % path
            )
        )

    @classmethod
    def vite_hmr_client(cls) -> Markup:
        tags = [
            dedent(
                """
                <script type="module" src="http://localhost:5173/@vite/client"></script>
                """
            )
        ]
        if Rizzler._framework == "react":
            tags.append(
                dedent(
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
            )
        return Markup("\n".join(tags))


__all__: tuple[str, ...] = ("RizzleTemplates",)
