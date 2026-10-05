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

### Standard packages ###
from importlib import import_module, reload

### Third-party packages ###
from pytest import raises
from pytest_mock import MockerFixture

### Local modules ###
from rizzler.exceptions import MissingTemplateBackendError


def test_missing_template_backends(mocker: MockerFixture) -> None:
    mocker.patch.dict("sys.modules", {"jinja2": None, "minijinja": None})
    reload(import_module("rizzler.templating"))
    from rizzler.templating import RizzleTemplates

    with raises(MissingTemplateBackendError) as exc_info:
        RizzleTemplates(directory="templates")
    message = str(exc_info.value)
    assert "rizzler[jinja2]" in message
    assert "rizzler[minijinja]" in message

    mocker.stopall()
    reload(import_module("rizzler.templating"))
