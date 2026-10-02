#!/usr/bin/env python3.10
"""
Type stubs for minijinja for Environment, load_from_path and pass_state
"""

from os import PathLike
from typing import Callable, Sequence, TypeVar
from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

class Environment:
    """Represents a MiniJinja environment"""
    # pub fn eval_expr(
    #     slf: PyRef<'_, Self>,
    #     py: Python<'_>,
    #     expression: &str,
    #     ctx: Option<&Bound<'_, PyDict>>,
    # ) -> PyResult<Py<PyAny>>
    def eval_expr(self, *args: P.args, **kwargs: P.kwargs): ...

    # pub fn render_str(
    #     slf: PyRef<'_, Self>,
    #     py: Python<'_>,
    #     source: &str,
    #     name: Option<&str>,
    #     ctx: Option<&Bound<'_, PyDict>>,
    # ) -> PyResult<String>
    def render_str(self, *args: P.args, **kwargs: P.kwargs): ...

    # pub fn render_template(
    #     slf: PyRef<'_, Self>,
    #     py: Python<'_>,
    #     template_name: &str,
    #     ctx: Option<&Bound<'_, PyDict>>,
    # ) -> PyResult<String>
    def render_template(self, *args: P.args, **kwargs: P.kwargs) -> str: ...

def load_from_path(
    paths: str | PathLike[str] | Sequence[str | PathLike[str]] | None = None,
):
    """Load a template from one or more paths."""

def pass_state(f: Callable[P, R]) -> Callable[P, R]:
    """Pass the engine state to the function as first argument."""

__all__: tuple[str, ...] = ("Environment", "load_from_path", "pass_state")
