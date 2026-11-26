import pytest
from pydantic import ValidationError

from presales.core.config import Settings


def test_database_url_defaults() -> None:
    s = Settings(_env_file=None, postgres_password="pw")
    assert s.database_url == "postgresql://presales:pw@localhost:5432/presales"


def test_password_is_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_password_hidden_in_repr() -> None:
    assert "secret123" not in repr(Settings(_env_file=None, postgres_password="secret123"))


def test_special_characters_are_url_encoded() -> None:
    s = Settings(_env_file=None, postgres_password="p@ss/w:rd")
    assert "p%40ss%2Fw%3Ard" in s.database_url
