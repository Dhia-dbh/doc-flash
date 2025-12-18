# DocFlash

FastAPI service that adds documentation, generates markdown walkthroughs, and proposes tests for source code using pluggable LLM providers (Gemini-first).

## Features

- Annotate code with docstrings and inline intent comments without changing behaviour.
- Produce developer-focused markdown summaries as downloadable `text/markdown` (custom filename via payload).
- Generate pytest-style unit tests to seed coverage from a snippet.
- Swap providers via `DOCFLASH_LLM_PROVIDER` (`gemini` or `mock`); `/health` shows the active provider.
- Centralised prompts and provider factory keep the FastAPI layer thin and async-friendly.

## Quickstart

```bash
poetry install
cp .env.example .env  # add your GEMINI_API_KEY or DOCFLASH_GEMINI_API_KEY
poetry run uvicorn doc_flash.main:app --reload
```

Set `DOCFLASH_LLM_PROVIDER=mock` in `.env` to run locally without external LLM calls.

## Configuration

Environment variables (prefix `DOCFLASH_` unless noted):

- `APP_NAME` (default `DocFlash`)
- `LLM_PROVIDER` (`gemini` | `mock`)
- `GEMINI_API_KEY` or `DOCFLASH_GEMINI_API_KEY` (required for `gemini`)
- `GEMINI_MODEL` (default `gemini-2.5-flash`)
- `TEMPERATURE` (default `0.2`)

## API

Base URL: `http://localhost:8000`

Shared payload:

```json
{"code": "def add(a, b):\n    return a + b", "filename": "optional-markdown-name.md"}
```

### Document code

`POST /v1/document` → JSON `{ "documented_code": "<annotated code>" }`

```bash
curl -X POST http://localhost:8000/v1/document \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a, b):\n    return a + b"}'
```

### Generate markdown summary

`POST /v1/markdown` → `text/markdown` with `Content-Disposition` attachment header (defaults to `code_overview.md` unless `filename` is provided).

```bash
curl -X POST http://localhost:8000/v1/markdown \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a, b):\n    return a + b", "filename": "add_overview.md"}' -OJ
```

### Generate pytest tests

`POST /v1/tests` → JSON `{ "tests_code": "<pytest file contents>" }`

```bash
curl -X POST http://localhost:8000/v1/tests \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a, b):\n    return a + b"}'
```

### Health check

`GET /health` → `{"status": "ok", "provider": "<gemini|mock>"}`

## Notebook

`notebooks/gemini_doc_demo.ipynb` walks through configuring Gemini and calling the documentation and markdown prompts directly; you can reuse the same client to call the tests prompt if needed.

## Design notes

- Strategy pattern via `LLMProvider` now covers documentation, markdown descriptions, and test generation.
- Provider instances are cached and warmed on startup so misconfiguration fails fast.
- Prompts live in `doc_flash/services/prompts.py` to keep provider logic focused on transport.
