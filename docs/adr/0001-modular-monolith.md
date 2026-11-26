# ADR 0001: Modular monolith
- Status: accepted
- Date: 2026-11-24

## Context
Small team, internal tool, one shared database, and pipeline stages that depend closely on each other.

## Options considered
1. Microservices.
2. One deployable application with strict internal module boundaries.

## Decision
Option 2: Streamlit, FastAPI, PostgreSQL + pgvector, and LangGraph in one deployable. One folder per
pipeline stage under `src/presales/`. API and UI contain no business logic.

## Consequences
Simple operations and transactions. Revisit only if a module needs independent scaling
(model serving is the likely first candidate).