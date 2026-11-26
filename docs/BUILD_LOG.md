# Build Log
Newest first. Each entry: what changed, why, how it was verified, problems and fixes, open items.

## 2026-11-26 - Phase 0: core config, design decisions, ADRs
**Changed**
- `core/config.py`: typed settings via pydantic-settings, read from `.env`. Database password is required (no default) and masked in output; `database_url` URL-encodes special characters; `get_settings()` is cached.
- Default Postgres port in code is 5432 (the standard); the laptop's `.env` overrides it to 5433.
- `tests/unit/test_config.py`: defaults, required password, password hidden in repr, URL encoding.
- ADRs 0001-0007 written in `docs/adr/` (modular monolith, deterministic sizing, LLM provider abstraction, hybrid retrieval, LangGraph for orchestration only, documentation policy, multi-user access and isolation).
- pgAdmin connects to the container (host 127.0.0.1, port 5433, database and user `presales`). Extensions listed: plpgsql 1.0, vector 0.8.7. No tables yet.

**Decided**
- Knowledge base is shared by all users; chat sessions are private per user; every user logs in with their own account.
- One Postgres database with `user_id` on private rows, enforced by Row-Level Security (not one database per user). See ADR 0007.
- Uploaded RFPs and derived data are private to the uploader by default (sharing via a `case_members` table later). Proposed, pending confirmation.
- Raw uploaded files are stored outside the database (by SHA-256); only a pointer is kept in Postgres.
- Settings are added to `config.py` in the step that first uses them, not declared in advance.

**Verified**
- `python -m pytest -q`: 4 passed.
- `python -c` check: `localhost 5433 presales **********` (port override from `.env` works, password masked).

**Problems hit and fixes**
- `pytest.exe` was blocked by the organization's Device Guard policy. Workaround: run tools as Python modules (`python -m pytest`, `python -m mypy`). Compiled tools such as `ruff` may also be blocked; fallback is flake8 or an IT exception.

**Open items**
- Auth provider: local accounts first (proposed), Microsoft Entra SSO later if IT approves.
- SQLAlchemy 2.0 + Alembic versus raw SQL for migrations (proposed: SQLAlchemy + Alembic).
- `mypy` and `ruff` not yet run on this code.
- Logging module: format, destination, and what must never be logged still to be decided.
- LLM provider and model not chosen. Embedding model default bge-m3 (1024 dims). BM25 approach (`tsvector` vs extension) not decided.

## 2026-11-25 - Phase 0: environment and database
**Changed**
- Project structure (src layout, one module per pipeline stage); Git repo on GitHub (private).
- Python 3.12.10 venv; `requirements.txt` (runtime), `requirements-dev.txt` (tooling), `requirements.lock` (exact versions), `pyproject.toml` (makes `src/presales` importable).
- `docker-compose.yml`: `pgvector/pgvector:pg17`, healthcheck, data volume, published on 127.0.0.1 only.
- `infra/db/init.sql` enables the `vector` extension. `.env` (not committed) holds credentials; `.env.example` is the template.
- Project moved out of OneDrive to `C:\Users\Admin\Downloads\presales-agent` (OneDrive would sync `.venv` and `.git`; the `&` in the old folder name breaks scripts).

**Why**
- Docker Desktop on the laptop so the database matches how it will run on a server.
- Port bound to localhost so the database is not reachable from the network.

**Verified**
- All packages import (pydantic 2.14.4). Container healthy. `pg_extension` query returns `vector 0.8.7`. Port shown as `127.0.0.1:5433->5432/tcp`.

**Problems hit and fixes**
- Docker install failed: Virtual Machine Platform was disabled. Fixed with an all-users installation (WSL 2 backend) and a WSL update.
- Compose warned "variable is not set": `.env` was copied while `.env.example` was still empty. Filled in `.env`, ran `docker compose down -v`, restarted.
- Compose failed with "ports are not available" on 5432. Cause: a native Windows Postgres service (`postgres.exe`, PID 8808) already listens on 5432. Fix: project database published on 127.0.0.1:5433 (`POSTGRES_PORT=5433`). Do not stop the native Postgres.