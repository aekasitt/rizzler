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

Voila! Now you have a production front-end to go with your `FastAPI` application when you need.
There will probably be bugs when it comes to relative versus absolute paths in the future.
But this is good enough for many prototyping use-case and with a bit of tinkering, can replace 

## Contributions

To be determined.

## Acknowledgements

* [fastapi-vite](https://github.com/cofin/fastapi-vite)
* [django-vite](https://github.com/MrBin99/django-vite)

## License

This project is licensed under the terms of the MIT license.
