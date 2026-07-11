import pytest

from app.db_config import DatabaseConfigError, build_database_url, read_database_settings


def test_build_database_url_from_environment(monkeypatch):
    monkeypatch.setenv("DB_HOST", "127.0.0.1")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "app_db")
    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.setenv("DB_PASSWORD", "postgres")

    assert build_database_url("DB") == "postgresql://postgres:postgres@127.0.0.1:5432/app_db"


def test_build_database_url_requires_all_database_settings(monkeypatch):
    monkeypatch.delenv("DB_HOST", raising=False)
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "app_db")
    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.setenv("DB_PASSWORD", "postgres")

    with pytest.raises(DatabaseConfigError, match="DB_HOST"):
        build_database_url("DB")


def test_test_database_settings_are_required(monkeypatch):
    monkeypatch.delenv("TEST_DB_NAME", raising=False)
    monkeypatch.setenv("TEST_DB_HOST", "127.0.0.1")
    monkeypatch.setenv("TEST_DB_PORT", "5432")
    monkeypatch.setenv("TEST_DB_USER", "postgres")
    monkeypatch.setenv("TEST_DB_PASSWORD", "postgres")

    with pytest.raises(DatabaseConfigError, match="TEST_DB_NAME"):
        read_database_settings("TEST_DB")
