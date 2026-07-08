import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

REQUIRED_DATABASE_ENV_VARS = (
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
)


def _require_database_settings() -> dict[str, str]:
    settings = {name: os.getenv(name) for name in REQUIRED_DATABASE_ENV_VARS}
    missing = [name for name, value in settings.items() if not value]
    if missing:
        raise RuntimeError(
            "Missing required database environment variables: "
            + ", ".join(missing)
        )
    return {name: value for name, value in settings.items() if value is not None}


def build_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    settings = _require_database_settings()
    try:
        port = int(settings["DB_PORT"])
    except ValueError as exc:
        raise RuntimeError("DB_PORT must be an integer.") from exc

    username = quote_plus(settings["DB_USER"])
    password = quote_plus(settings["DB_PASSWORD"])
    host = settings["DB_HOST"]
    database = quote_plus(settings["DB_NAME"])

    return f"postgresql://{username}:{password}@{host}:{port}/{database}"


DATABASE_URL = build_database_url()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
