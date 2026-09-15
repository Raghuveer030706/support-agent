# support-agent

## Setup

```bash
uv sync
cp .env.example .env
```

## Run

```bash
uv run uvicorn app.main:app --reload --app-dir src
```

## Test

```bash
uv run pytest
```
