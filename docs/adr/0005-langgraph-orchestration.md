# ADR 0005: LangGraph for orchestration only
- Status: accepted
- Date: 2026-11-25

## Context
The workflow branches, loops (retry extraction, re-run gap check after new answers), and pauses for
humans (clarification answers, approval before proposals leave the system).

## Decision
LangGraph handles control flow, retries, human-in-the-loop interrupts, and Postgres checkpointing.
Graph nodes are thin wrappers over plain, separately testable functions. No free-roaming multi-agent
loops; bounded agent steps only where justified. Large artifacts live in the database, and graph state
holds only identifiers and summaries.

## Consequences
Durable pause and resume. Node names and state fields must stay backward compatible across deployments
(or cases are pinned to a graph version). Nodes must be safe to re-run.