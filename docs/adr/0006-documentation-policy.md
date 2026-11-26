# ADR 0006: Documentation policy
- Status: accepted
- Date: 2026-11-25

## Context
The project is intended for real office use, and everything done on it must be documented.

## Decision
Documentation lives in the repository and is committed together with the code. Every change set gets a
BUILD_LOG entry stating what was changed, why, how it was verified, and what was not verified. Every
non-obvious decision gets an ADR the same day. ARCHITECTURE and ROADMAP are kept current.

## Consequences
Small ongoing effort per change in exchange for a readable history and onboarding path.