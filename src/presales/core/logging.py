"""Structured logging for the whole application.

Console output in dev, JSON lines in prod (stdout only). Third-party libraries that use the
standard `logging` module (uvicorn, SQLAlchemy, ...) go through the same pipeline, so every
line has the same shape.

Privacy rule: log identifiers and sizes, never document text, prompts, or credentials.
`redact_sensitive` is a safety net for that rule, not a substitute for following it.
"""

from __future__ import annotations

import logging
import sys
from collections.abc import MutableMapping
from typing import Any

import structlog

# Field names whose values must never reach a log line.
SENSITIVE_KEYS = frozenset(
    {
        "password",
        "passwd",
        "secret",
        "token",
        "access_token",
        "refresh_token",
        "authorization",
        "api_key",
        "cookie",
        "text",
        "content",
        "prompt",
        "response",
        "completion",
        "document_text",
        "chunk_text",
    }
)
REDACTED = "[REDACTED]"


def redact_sensitive(
    _logger: Any, _method: str, event_dict: MutableMapping[str, Any]
) -> MutableMapping[str, Any]:
    """Replace values of sensitive top-level fields. Nested structures are not inspected."""
    for key in event_dict:
        if key.lower() in SENSITIVE_KEYS:
            event_dict[key] = REDACTED
    return event_dict


def configure_logging(level: str = "INFO", json_output: bool = False) -> None:
    """Call once at process start (API startup, CLI entry point)."""
    shared: list[Any] = [
        structlog.contextvars.merge_contextvars,  # request_id / user_id / case_id
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        redact_sensitive,
    ]
    structlog.configure(
        processors=[*shared, structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
    )

    renderer: Any = (
        structlog.processors.JSONRenderer() if json_output else structlog.dev.ConsoleRenderer()
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=shared,  # applies the same fields to stdlib/third-party records
            processors=[structlog.stdlib.ProcessorFormatter.remove_processors_meta, renderer],
        )
    )
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level.upper())


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.stdlib.get_logger(name)


def bind_context(**fields: Any) -> None:
    """Attach fields (request_id, user_id, case_id) to every log line in this request/task."""
    structlog.contextvars.bind_contextvars(**fields)


def clear_context() -> None:
    structlog.contextvars.clear_contextvars()
