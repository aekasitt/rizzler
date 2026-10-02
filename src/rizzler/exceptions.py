#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2024-2026, All rights reserved.
# FILENAME:    ~~/src/rizzler/exceptions.py
# VERSION:     0.2.1
# CREATED:     2026-10-01 17:36:35 +0700
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************


class RizzlerException(Exception): ...


class MissingTemplateBackendError(RizzlerException): ...


__all__: tuple[str, ...] = ("MissingTemplateBackendError", "RizzlerException")
