# ADR 0002: Sizing and BOM are deterministic code
- Status: accepted
- Date: 2026-11-25

## Context
Sizing (capacity from data size, change rate, retention, compression; component counts) is arithmetic
plus vendor rules. Its results go into customer proposals and must be reproducible and auditable.

## Options considered
1. Let the LLM compute sizing and BOM.
2. LLM extracts requirements and writes prose; code computes all numbers.

## Decision
Option 2. Sizing rules are versioned, unit-tested code. The rules version is recorded on every
sizing run and BOM.

## Consequences
Reproducible, testable results. Cost: rules must be written and maintained per vendor and product version.