#!/usr/bin/env python3.10
"""
Type stubs for starlette for TemplateResponse and _TemplateResponse
"""

from typing import Any
from starlette.responses import HTMLResponse

class _TemplateResponse(HTMLResponse): ...

class Jinja2Templates:
    def TemplateResponse(self, *args: Any, **kwargs: Any) -> _TemplateResponse: ...

__all__: tuple[str, ...] = ("Jinja2Templates", "_TemplateResponse")
