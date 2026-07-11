import os
from urllib.parse import quote_plus

REQUIRED_DATABASE_SETTING_NAMES = (
    "HOST",
    "PORT",
    "NAME",
    "USER",
    "PASSWORD",
)


class DatabaseConfigError(RuntimeError):
    pass


def required_database_env_vars(prefix: str = "DB") -> tuple[str, ...]:
    return tuple(f"{prefix}_{name}" for name in REQUIRED_DATABASE_SETTING_NAMES)


def read_database_settings(prefix: str = "DB") -> dict[str, str]:
    required_vars = required_database_env_vars(prefix)
    settings = {name: os.getenv(name) for name in required_vars}
    missing = [name for name, value in settings.items() if not value]
    if missing:
        raise DatabaseConfigError(
            "Missing required database environment variables: "
            + ", ".join(missing)
        )
    return {name: value for name, value in settings.items() if value is not None}


def build_database_url(prefix: str = "DB") -> str:
    settings = read_database_settings(prefix)
    port_name = f"{prefix}_PORT"
    try:
        port = int(settings[port_name])
    except ValueError as exc:
        raise DatabaseConfigError(f"{port_name} must be an integer.") from exc

    username = quote_plus(settings[f"{prefix}_USER"])
    password = quote_plus(settings[f"{prefix}_PASSWORD"])
    host = settings[f"{prefix}_HOST"]
    database = quote_plus(settings[f"{prefix}_NAME"])

    return f"postgresql://{username}:{password}@{host}:{port}/{database}"
