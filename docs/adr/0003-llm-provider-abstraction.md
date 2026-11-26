# ADR 0003: Provider-agnostic LLM interface; provider choice deferred
- Status: accepted (interface); provider choice open
- Date: 2026-11-25

## Context
Real RFPs may not be allowed to leave the company network, and the quality of local models on
extraction is not yet measured.

## Options considered
1. Cloud API only. 2. Local (Ollama) only. 3. Hybrid.

## Decision
All code uses one LLM interface, and the provider is chosen by configuration. Develop on synthetic or
anonymized documents, run the same extraction evaluation on a cloud and a local model, then choose
by data policy and measured accuracy. A hybrid (local for raw documents, cloud only for sanitized
structured data) is an allowed outcome.

## Consequences
Switching is a configuration change. An extraction evaluation set must exist before the final choice.