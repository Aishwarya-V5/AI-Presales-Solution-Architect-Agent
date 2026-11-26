# ADR 0007: Multi-user access, authentication, and data isolation
- Status: accepted (isolation model, shared KB); proposed (auth provider, case sharing)
- Date: 2026-11-26

## Context
Several users log in with their own accounts. The knowledge base is shared by all users.
Chat sessions are private per user. Uploaded RFPs and derived data are customer-confidential.

## Options considered
1. Database per user: breaks the shared KB, multiplies migrations, pools and indexes by N.
2. Schema per user: same problems, less severe.
3. One database, user_id on private rows, Postgres Row-Level Security (RLS).

## Decision
Option 3.
- Tables: users, cases, case_members, conversations, messages, memories, plus case data tables.
- KB tables are readable by all authenticated users, writable by admins only.
- conversations/messages/memories are owner-only. Cases are owner-only by default, shareable
  via case_members.
- Enforcement in three layers: FastAPI authenticates every request and derives user_id from
  the token; repository functions take the current user; Postgres RLS via
  `SET LOCAL app.user_id` per transaction.
- The application connects as a non-superuser role that does not own the tables; migrations
  use a separate owner role. FORCE ROW LEVEL SECURITY is set.
- Authentication: local accounts first (argon2 password hashes, JWT) behind an auth interface;
  Microsoft Entra ID OIDC added later if IT approves.
- LangGraph thread ids are scoped to a user; ownership is checked before resuming a thread.

## Consequences
- One migration path, one KB, easy sharing later.
- Required test: user A cannot read user B's cases, chunks, or chats through the API or raw SQL.
- Pooled connections must use SET LOCAL inside a transaction, never plain SET.
- Revisit if a customer requires physically separate storage per tenant.