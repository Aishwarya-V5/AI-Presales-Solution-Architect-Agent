# ADR 0004: Two-stage hybrid retrieval
- Status: accepted
- Date: 2026-11-24

## Context
The knowledge base is vendor documentation with tables, version-specific rules, and exact identifiers
(product names, SKUs). Dense vector search alone is weak on these.

## Decision
Stage 1: metadata hard filters (vendor, product, version, document type) plus pgvector dense search and
BM25/full-text search, fused with reciprocal rank fusion. Stage 2: cross-encoder reranker. Parent
section expansion before the LLM sees the context.

## Defaults pending confirmation
Embedding model bge-m3 (1024 dimensions). Lexical search via Postgres `tsvector` first; move to a BM25
extension only if evaluation shows lexical recall is the bottleneck.

## Consequences
Filters are applied inside both queries, not afterwards. The embedding model name is stored per chunk,
and changing the model means re-embedding. Recall after fusion and precision after reranking are
measured separately.