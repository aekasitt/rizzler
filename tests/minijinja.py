#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2024-2026, All rights reserved.
# FILENAME:    ~~/tests/minijinja.py
# VERSION:     0.2.0
# CREATED:     2026-10-02 13:06:41 +0700
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard library ###
from collections.abc import Generator
from importlib import import_module
from pathlib import Path
from tempfile import TemporaryDirectory

### Third-party packages ###
from pytest import fixture, importorskip, raises, warns
from starlette.datastructures import URLPath
from starlette.requests import Request

### Local modules ###
importorskip("minijinja")
RizzleTemplates = import_module("rizzler.templating.minijinja").RizzleTemplates


class _Router:
    def url_path_for(self, name: str, **path_params: object) -> URLPath:
        if name != "item":
            raise KeyError(name)
        return URLPath(f"/items/{path_params['item_id']}", protocol="http")


@fixture(scope="module")
def setup_teardown() -> Generator[tuple[Request, RizzleTemplates], None, None]:
    temporary_directory = TemporaryDirectory()
    directory = Path(temporary_directory.name)
    (directory / "index.html").write_text(
        "{{ title }} {{ url_for('item', item_id=7) }} "
        "{{ vite_asset('pages/main.js') }}",
        encoding="utf-8",
    )
    templates = RizzleTemplates(directory=directory)
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/",
            "root_path": "",
            "scheme": "http",
            "query_string": b"",
            "headers": [],
            "server": ("testserver", 80),
            "client": ("testclient", 50000),
            "extensions": {},
            "router": _Router(),
        }
    )
    yield request, templates
    temporary_directory.cleanup()


def test_template_response_renders_context_and_globals(setup_teardown) -> None:
    request, templates = setup_teardown
    response = templates.TemplateResponse(
        request,
        "index.html",
        {"title": "<Rizzler>"},
    )

    body = response.body.decode()
    assert "&lt;Rizzler&gt;" in body
    assert "http://testserver/items/7" in body
    assert 'src="http://localhost:5173/pages/main.js"' in body
    assert response.media_type == "text/html"
    assert response.template == "index.html"
    assert response.context["request"] is request


def test_legacy_call_requires_request_in_context(setup_teardown) -> None:
    _, templates = setup_teardown
    with warns(DeprecationWarning):
        with raises(ValueError, match='context must include a "request"'):
            templates.TemplateResponse("index.html", {"title": "Rizzler"})
