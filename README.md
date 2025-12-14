# DocFlash

FastAPI service that documents source code using pluggable LLM providers (Gemini first). It exposes two endpoints:

- `POST /v1/document` returns the code with added docstrings and inline comments.
- `POST /v1/markdown` streams a markdown description of the code (served as a downloadable `text/markdown` response).

An accompanying Jupyter notebook shows how to call Gemini directly for both tasks.

## Quickstart

```bash
poetry install
cp .env.example .env  # add your GEMINI_API_KEY
poetry run uvicorn doc_flash.main:app --reload
```

## Configuration

Environment variables (prefixed with `DOCFLASH_` in `.env`):

- `DOCFLASH_LLM_PROVIDER` (`gemini` | `mock`)
- `GEMINI_API_KEY` (required for `gemini`)
- `DOCFLASH_GEMINI_MODEL` (default `gemini-2.5-flash`)
- `DOCFLASH_TEMPERATURE` (default `0.2`)

Set `DOCFLASH_LLM_PROVIDER=mock` to run without external calls.

## API usage

Document code:

```bash
curl -X POST http://localhost:8000/v1/document \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a, b):\n    return a + b"}'
```

Generate markdown (downloads `code_overview.md` by default):

```bash
curl -X POST http://localhost:8000/v1/markdown \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a, b):\n    return a + b"}' -OJ
```

## Notebook

See `notebooks/gemini_doc_demo.ipynb` for a concise, titled walkthrough that:

- Configures the free-tier Gemini client with your `GEMINI_API_KEY`.
- Sends one prompt to document code.
- Sends another prompt to generate markdown.

## Design notes

- Strategy pattern via `LLMProvider` allows swapping providers (Gemini or mock) without touching the API layer.
- Provider instances are cached during startup; misconfiguration fails fast.
- Prompts are centralised in `app/services/prompts.py` to keep provider logic thin.
