#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2024-2026, All rights reserved.
# FILENAME:    ~~/src/rizzler/templating/__init__.py
# VERSION:     0.2.0
# CREATED:     2024-06-07 01:39 +0700
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************

### Local modules ###
from rizzler.exceptions import MissingTemplateBackendError

try:
    import minijinja
except ModuleNotFoundError as error:
    if error.name != "minijinja":
        raise

    try:
        import jinja2
        import starlette.templating
    except ModuleNotFoundError as error:
        if error.name not in {"jinja2", "starlette", "starlette.templating"}:
            raise

        class RizzleTemplates:
            def __init__(self, *args: object, **kwargs: object) -> None:
                raise MissingTemplateBackendError(
                    "RizzleTemplates requires a template backend. "
                    "Install the recommended backend with `pip install "
                    '"rizzler[jinja2]"`, or use MiniJinja with `pip install '
                    '"rizzler[minijinja]"`.'
                ) from None
    else:
        from rizzler.templating.jinja2 import RizzleTemplates
else:
    from rizzler.templating.minijinja import RizzleTemplates


__all__: tuple[str, ...] = ("RizzleTemplates",)
