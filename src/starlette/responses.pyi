#!/usr/bin/env python3.10
"""
Type stubs for starlette for HTMLResponse, Response
"""

### Standard packages ###
from typing import Mapping

class Response:
    media_type: None | str = None
    charset: str = "utf-8"

    def __init__(
        self,
        content: bytes | str | memoryview,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: None | str = None,
    ) -> None: ...

class HTMLResponse(Response):
    media_type = "text/html"

__all__: tuple[str, ...] = ("HTMLResponse", "Response")
