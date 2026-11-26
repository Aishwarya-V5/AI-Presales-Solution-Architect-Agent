import json
import logging
from collections.abc import Iterator

import pytest

from presales.core.logging import (
    bind_context,
    clear_context,
    configure_logging,
    get_logger,
)


@pytest.fixture(autouse=True)
def _clean_context() -> Iterator[None]:
    clear_context()
    yield
    clear_context()


def _last_json(capsys: pytest.CaptureFixture[str]) -> dict[str, object]:
    lines = [ln for ln in capsys.readouterr().out.splitlines() if ln.strip()]
    return json.loads(lines[-1])  # type: ignore[no-any-return]


def test_json_output_has_standard_fields(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging("INFO", json_output=True)
    get_logger("t").info("doc_parsed", document_id=12, pages=42)
    data = _last_json(capsys)
    assert data["event"] == "doc_parsed"
    assert data["document_id"] == 12
    assert data["level"] == "info"
    assert data["logger"] == "t"
    assert "timestamp" in data


def test_level_filters_debug(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging("INFO", json_output=True)
    get_logger("t").debug("hidden")
    assert capsys.readouterr().out == ""


def test_sensitive_values_are_redacted(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging("INFO", json_output=True)
    get_logger("t").info("x", password="hunter2", prompt="customer ACME needs...", pages=3)
    data = _last_json(capsys)
    assert data["password"] == "[REDACTED]"
    assert data["prompt"] == "[REDACTED]"
    assert data["pages"] == 3
    assert "hunter2" not in json.dumps(data)


def test_context_is_attached_and_clearable(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging("INFO", json_output=True)
    bind_context(request_id="r1", user_id=3, case_id=7)
    get_logger("t").info("a")
    data = _last_json(capsys)
    assert (data["request_id"], data["user_id"], data["case_id"]) == ("r1", 3, 7)
    clear_context()
    get_logger("t").info("b")
    assert "request_id" not in _last_json(capsys)


def test_stdlib_logger_uses_same_format(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging("INFO", json_output=True)
    logging.getLogger("uvicorn.error").warning("third party message")
    data = _last_json(capsys)
    assert data["event"] == "third party message"
    assert data["level"] == "warning"
