"""Typed application settings, loaded once from environment variables / .env."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal
from urllib.parse import quote

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # .env is resolved relative to the working directory: run commands from the repo root.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: Literal["dev", "staging", "prod"] = "dev"
    log_level: str = "INFO"
    log_json: bool = False

    postgres_user: str = "presales"
    # No default on purpose: a missing password must fail at startup, not at first query.
    postgres_password: SecretStr
    postgres_db: str = "presales"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    @property
    def database_url(self) -> str:
        # quote() keeps special characters in the password from breaking the URL.
        user = quote(self.postgres_user, safe="")
        password = quote(self.postgres_password.get_secret_value(), safe="")
        return (
            f"postgresql://{user}:{password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    """Cached accessor. Use this everywhere instead of constructing Settings()."""
    return Settings()
