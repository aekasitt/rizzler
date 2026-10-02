#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2024-2026, All rights reserved.
# FILENAME:    ~~/tests/empty.py
# VERSION:     0.2.0
# CREATED:     2026-10-02 13:06:41 +0700
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard library ###
from subprocess import run
from sys import executable
from textwrap import dedent


def test_missing_template_backends_raise_installation_error() -> None:
    script = dedent(
        """
        import builtins

        real_import = builtins.__import__

        def import_without_template_backends(name, *args, **kwargs):
            if name in {"jinja2", "minijinja"}:
                error = ModuleNotFoundError(f"No module named '{name}'")
                error.name = name
                raise error
            return real_import(name, *args, **kwargs)

        builtins.__import__ = import_without_template_backends

        from rizzler import RizzleTemplates
        from rizzler.exceptions import MissingTemplateBackendError

        try:
            RizzleTemplates(directory="templates")
        except MissingTemplateBackendError as error:
            message = str(error)
            assert "rizzler[jinja2]" in message
            assert "rizzler[minijinja]" in message
        else:
            raise AssertionError("MissingTemplateBackendError was not raised")
        """
    )

    run([executable, "-c", script], check=True)
