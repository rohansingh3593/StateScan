#!/bin/sh
set -eu

echo "Checking standalone PostgreSQL service"
echo "Waiting for database readiness"
python scripts/wait_for_database.py
echo "Database connection validated"

echo "Running pytest test suite"
pytest -v tests

echo "Test execution summary: pytest completed successfully"
echo "Starting FastAPI application"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
