# FastAPI + SQLAlchemy + Docker

This project provides a simple FastAPI application with SQLAlchemy and PostgreSQL, containerized with Docker Compose.

## Project Structure

```text
StateScan/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── __init__.py
├── scripts/
│   ├── start.sh
│   └── wait_for_database.py
├── tests/
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```


## PostgreSQL Docker Configuration

Docker Compose runs PostgreSQL as a dedicated `db` container and the FastAPI app as a separate `web` container on a shared Docker bridge network. The `web` service connects to PostgreSQL using the `db` service name as its database host, and the `postgres_data` Docker volume preserves database files across container restarts. The PostgreSQL startup script also creates a separate test database so pytest never writes test data into the application database.

Database configuration is provided through environment variables. Copy the example file before starting the stack if you want to customize the defaults:

```bash
cp .env.example .env
```

Required database environment variables:

| Variable | Default | Description |
| --- | --- | --- |
| `DB_HOST` | `db` | PostgreSQL hostname used by the FastAPI container. |
| `DB_PORT` | `5432` | PostgreSQL port used by the FastAPI container. |
| `DB_NAME` | `app_db` | Application database created by the PostgreSQL container. |
| `DB_USER` | `postgres` | PostgreSQL username for the application database. |
| `DB_PASSWORD` | `postgres` | PostgreSQL password for the application database. |
| `TEST_DB_HOST` | `db` | PostgreSQL hostname used by pytest inside Docker. |
| `TEST_DB_PORT` | `5432` | PostgreSQL port used by pytest inside Docker. |
| `TEST_DB_NAME` | `test_db` | Dedicated test database created separately from the application database. |
| `TEST_DB_USER` | `postgres` | PostgreSQL username for the test database. |
| `TEST_DB_PASSWORD` | `postgres` | PostgreSQL password for the test database. |
| `DB_HOST_PORT` | `5432` | Optional host port for connecting from your machine. |

The application validates the required `DB_*` variables at startup and dynamically builds the SQLAlchemy connection URL from them. PostgreSQL initializes the application database through `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD`; `scripts/init-test-database.sh` creates the separate `TEST_DB_NAME` database during first-time PostgreSQL container initialization. If any required `DB_*` or `TEST_DB_*` value is missing, Docker Compose or the application/test startup fails with a clear configuration error instead of silently falling back to another database.

To verify the PostgreSQL container is running, use:

```bash
docker compose ps db
```

To connect from a database client on the Docker host with the default settings, use:

```text
Host: localhost
Port: 5432
Database: app_db
Username: postgres
Password: postgres
```

You can also open a `psql` shell inside the container:

```bash
docker compose exec db psql -U postgres -d app_db
```

## How to Run the Application

### Option 1: Run with Docker Compose

From the project root, run:

```bash
docker compose up --build
```

This builds the FastAPI image, starts PostgreSQL, waits for the database health check, runs the complete `pytest -v tests` suite inside the application container, and starts FastAPI only if every test passes. The container logs show each startup stage:

1. Starting database service
2. Waiting for database readiness
3. Running pytest test suite
4. Test execution summary
5. Starting FastAPI application

If any test fails, pytest exits with a non-zero status code, the failure report remains visible in the Docker logs, and the FastAPI application is not started. Fix the failing test or application code, then run `docker compose up --build` again.

Once the tests pass and the app starts, open:

- http://<your-machine-ip>:9000/health
- http://<your-machine-ip>:9000/items
- http://<your-machine-ip>:9000/docs

### Option 2: Run Locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Set the local database environment variables. If PostgreSQL is exposed from Docker Compose on the default host port, use `localhost` as the host:

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=app_db
export TEST_DB_HOST=localhost
export TEST_DB_PORT=5432
export TEST_DB_NAME=test_db
export TEST_DB_USER=postgres
export TEST_DB_PASSWORD=postgres
export DB_USER=postgres
export DB_PASSWORD=postgres
```

Start the app:

```bash
uvicorn app.main:app --reload
```

The app will be available at:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/items
- http://127.0.0.1:8000/docs


## Running Tests Manually

Docker Compose runs the automated test suite during application startup. To run the same tests manually on your machine, install dependencies and run:

```bash
pytest -v tests
```

To run tests manually inside a running Docker container, use the application service name `web`:

```bash
docker compose exec web pytest -v tests
```

When Docker startup fails during the test stage, inspect the `web` service logs. Pytest prints the failing test name, assertion or exception details, and a final summary showing passed, failed, and skipped tests. The FastAPI server starts only after this command exits successfully.

### Stop the containers

```bash
docker compose down
```

## Running Tests with PowerShell

A PowerShell test runner is available at `testcase.ps1`.

From the `StateScan` directory, run:

```powershell
cd "C:\Users\rohan\repos\Notebook-main\Notebook-main\Docker Project\StateScan"
.\testcase.ps1 -Verbose
```

If you need to install dependencies first:

```powershell
.\testcase.ps1 -InstallDependencies -Verbose
```

This script runs `pytest` against the `tests/` folder and prints detailed output.

## Example Requests

### Create an item

```bash
curl -X POST "http://<your-machine-ip>:9000/items" -H "Content-Type: application/json" -d '{"name":"sample item"}'
```

### List items

```bash
curl "http://<your-machine-ip>:9000/items"
```
