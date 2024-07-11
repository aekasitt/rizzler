# Rizzler

[![Package vesion](https://img.shields.io/pypi/v/rizzler)](https://pypi.org/project/rizzler)
[![Format](https://img.shields.io/pypi/format/rizzler)](https://pypi.org/project/rizzler)
[![Python version](https://img.shields.io/pypi/pyversions/rizzler)](https://pypi.org/project/rizzler)
[![License](https://img.shields.io/pypi/l/rizzler)](https://pypi.org/project/rizzler)
[![Code size](https://img.shields.io/github/languages/code-size/aekasitt/rizzler)](.)
[![Top](https://img.shields.io/github/languages/top/aekasitt/rizzler)](.)
[![Languages](https://img.shields.io/github/languages/count/aekasitt/rizzler)](.)
[![Repository size](https://img.shields.io/github/repo-size/aekasitt/rizzler)](.)
[![Last commit](https://img.shields.io/github/last-commit/aekasitt/rizzler/master)](.)
[![Rizzler Banner](./static/rizzler-banner.svg)](https://github.com/aekasitt/rizzler/blob/master/static/rizzler-banner.svg)

## Installation

Install using pip

```sh
$ pip install rizzler
> ...
```

## Usage

Integrate with `lifespan` protocol.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.requests impor Request
from fastapi.responses import HTMLResponse
from rizzler import RizzleTemplates, Rizzler
from typing import AsyncIterator, List, Tuple

@Rizzler.load_config
def rizzler_settings() -> List[Tuple[str, str]]:
  return [
    ("command", "pnpm"),
    ("framework", "vue")
  ]

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None, None]:
  await Rizzler.serve()
  yield
  Rizzler.shutdown()

app: FastAPI = FastAPI(lifespan=lifespan)
templates: RizzleTemplates = RizzleTemplates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
  return templates.TemplateResponse("index.html", {"request": request})
```

### Templating

`RizzleTemplates` is an extension on top of `Jinja2Templates` class found under [starlette](starlette.io)
However, has two overriding methods that must be placed inside the template HTML-file as such:

```html
<!DOCTYPE html>
<html>
  <head><!-- ... --></head>
  <body>
    {{ vite_hmr_client() }}
    {{ vite_asset('pages/main.js') }}
  </body>
</html>
```

## Build

You can run the following command once you are done customizing the front-end code under `pages/` directory
to your liking.

```sh
rzl build
```

<details>
  <summary>Example outputs for `rzl build`</summary>

  ```sh
  $ rzl build
  > INFO     ⚡Building Rizzler front-end…
  > INFO
  > INFO     > rzl-tmp@0.0.0 build /Users/mackasitt/workspaces/rzl-react
  > INFO     > vite build                                       
  > INFO                                                       
  > INFO     vite v5.3.3 building for production...           
  > INFO     transforming...                                 
  > INFO     ✓ 32 modules transformed.                      
  > INFO     rendering chunks...                           
  > INFO     computing gzip size...                       
  > INFO     dist/rizz.svg    4.13 kB │ gzip:  2.14 kB   
  > INFO     dist/rizz.css    1.39 kB │ gzip:  0.72 kB  
  > INFO     dist/rizz.js   142.63 kB │ gzip: 45.74 kB 
  > INFO     ✓ built in 390ms
  ```
</details>

Now you can stop using `RizzleTemplates` and revert back to serving front-end with `Jinja2Templates`
as such

```python
#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="dist")

@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
  return templates.TemplateResponse("index.html", {"request": request})

app.mount("/", StaticFiles(directory="dist"), name="dist")
```

Now you have a production front-end to go with your `FastAPI` application when you need.
There will probably be bugs when it comes to relative versus absolute paths in the future.
But this is good enough for many prototyping use-case and with a bit of tinkering, can replace 

## Dependencies and Disclosures

This library relies on the following Python dependencies.

- **click** - Python composable command line interface toolkit 
  [![GitHub](https://img.shields.io/badge/-GitHub:%20pallets%2fclick-2B3137?logo=github&logoColor=white)](https://github.com/pallets/click)
  [![PyPI](https://img.shields.io/badge/-PyPI:%20click-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/click)
  [![Docs](https://img.shields.io/badge/-Sphinx:%20click-0A507A?logo=sphinx&logoColor=white)](https://click.palletsprojects.com/en/8.1.x)
- **jinja2** - A very fast and expressive template engine
  [![GitHub](https://img.shields.io/badge/-GitHub:%20pallets%2fjinja-2B3137?logo=github&logoColor=white)](https://github.com/pallets/jinja)
  [![PyPI](https://img.shields.io/badge/-PyPI:%20jinja2-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/click)
  [![Docs](https://img.shields.io/badge/-Sphinx:%20jinja2-0A507A?logo=sphinx&logoColor=white)](https://jinja.palletsprojects.com/en/3.1.x)
- **markupsafe** - Safely add untrusted strings to HTML/XML markup
  [![GitHub](https://img.shields.io/badge/-GitHub:%20pallets%2fmarkupsafe-2B3137?logo=github&logoColor=white)](https://github.com/pallets/markupsafe)
  [![PyPI](https://img.shields.io/badge/-PyPI:%20markupsafe-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/click)
  [![Docs](https://img.shields.io/badge/-Sphinx:%20markupsafe-0A507A?logo=sphinx&logoColor=white)](https://markupsafe.palletsprojects.com/en/2.1.x)

## Contributions

### Prerequisites


I recommend using `pyenv` and `poetry` as the preferred tools to managing this project.

- **pyenv**  - Simple Python version management 
  [![GitHub](https://img.shields.io/badge/GitHub-2B3137?logo=github&logoColor=white)](https://github.com/pyenv/pyenv)
  [![PyPI](https://img.shields.io/badge/-PyPI:%20pyenv-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/pyenv)
  [![OpenCollective](https://img.shields.io/badge/-OpenCollective:%20pyenv-7FADF2?logo=opencollective&logoColor=white)](https://opencollective.com/pyenv)
- **poetry** - Python packaging and dependency management made easy 
  [![GitHub](https://img.shields.io/badge/GitHub-2B3137?logo=github&logoColor=white)](https://github.com/python-poetry/poetry)
  [![PyPI](https://img.shields.io/badge/-PyPI:%20poetry-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/poetry)
  [![Poetry](https://img.shields.io/badge/-Poetry-60A5FA?logo=poetry&logoColor=white)](https://python-poetry.org)

### Setup development environment

To contribute to the project, fork the repository and clone to your local device and development
dependencies including four extra libraries not included in final builds as such:
Alternatively, run the following command on your terminal to do so:

```bash
poetry install --with dev
pytest
```

- **mypy** Optional static typing for Python
  [![GitHub](https://img.shields.io/badge/GitHub-2B3137?logo=github&logoColor=white)](https://github.com/python/mypy)
  [![PyPI](https://img.shields.io/badge/-PyPI:%20mypy-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/mypy)
  [![Docs](https://img.shields.io/readthedocs/mypy?logo=readthedocs)](https://mypy.readthedocs.io/en/stable/) 
- **pytest** The pytest framework makes it easy to write small tests, yet scales to support complex functional testing
  [![GitHub](https://img.shields.io/badge/GitHub-2B3137?logo=github&logoColor=white)](https://github.com/pytest-dev/pytest)
  [![PyPI](https://img.shields.io/badge/-PyPI:%20pytest-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/pytest)
  [![Docs](https://img.shields.io/badge/Sphinx-0A507A?logo=sphinx)](https://docs.pytest.org/en/latest)
- **ruff** An extremely fast Python linter and code formatter, written in Rust.
  [![GitHub](https://img.shields.io/badge/GitHub-2B3137?logo=github&logoColor=white)](https://github.com/astral-sh/ruff)
  [![PyPI](https://img.shields.io/badge/-PyPI:%20ruff-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/ruff)
  [![Docs](https://img.shields.io/badge/MkDocs-526CFE?logo=materialformkdocs&logoColor=white)](https://docs.astral.sh/ruff) 

## Acknowledgements

* [fastapi-vite](https://github.com/cofin/fastapi-vite)
* [django-vite](https://github.com/MrBin99/django-vite)

## License

This project is licensed under the terms of the MIT license.
