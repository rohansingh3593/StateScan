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


## Standalone PostgreSQL Docker Container

This project expects PostgreSQL to run as a standalone Docker container that you start manually before launching FastAPI. The application reads all database connection settings from environment variables and does not hardcode database host, port, name, username, or password.

### Start PostgreSQL manually

Create a persistent Docker volume once:

```bash
docker volume create statescan_postgres_data
```

Start the PostgreSQL container with PostgreSQL's official environment variable names (`POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD`):

```bash
docker run -d \
  --name statescan-postgres \
  --restart unless-stopped \
  -e POSTGRES_DB=app_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 127.0.0.1:5432:5432 \
  -v statescan_postgres_data:/var/lib/postgresql/data \
  postgres:16
```

With this command, PostgreSQL is available to host applications at:

```text
Host: 127.0.0.1
Port: 5432
Database: app_db
Username: postgres
Password: postgres
```

### Create the dedicated test database

The application database is `app_db`; pytest uses a separate `test_db` database so test data does not affect application data. After the container is running, create the test database once:

```bash
docker exec statescan-postgres psql -U postgres -d app_db -c "CREATE DATABASE test_db;"
```

If `test_db` already exists, PostgreSQL will report that it exists and you can continue.

### Verify PostgreSQL is running

Check the container status:

```bash
docker ps --filter name=statescan-postgres
```

Verify the configured application database accepts authenticated connections:

```bash
docker exec statescan-postgres psql -U postgres -d app_db -c "SELECT 1;"
```

Verify the test database exists:

```bash
docker exec statescan-postgres psql -U postgres -d app_db -c "SELECT datname FROM pg_database WHERE datname = 'test_db';"
```

### Configure environment variables

Copy the example environment file and adjust values if needed:

```bash
cp .env.example .env
```

Required application database variables:

| Variable | Example | Description |
| --- | --- | --- |
| `DB_HOST` | `127.0.0.1` | PostgreSQL host for local FastAPI runs. Use `host.docker.internal` when running FastAPI in Docker Compose against the standalone PostgreSQL container. |
| `DB_PORT` | `5432` | PostgreSQL port. |
| `DB_NAME` | `app_db` | Application database name. |
| `DB_USER` | `postgres` | Application database username. |
| `DB_PASSWORD` | `postgres` | Application database password. |

Required pytest database variables:

| Variable | Example | Description |
| --- | --- | --- |
| `TEST_DB_HOST` | `127.0.0.1` | PostgreSQL host for pytest. |
| `TEST_DB_PORT` | `5432` | PostgreSQL port for pytest. |
| `TEST_DB_NAME` | `test_db` | Dedicated pytest database name. |
| `TEST_DB_USER` | `postgres` | Test database username. |
| `TEST_DB_PASSWORD` | `postgres` | Test database password. |

The FastAPI startup script validates the database connection before running tests. If the standalone PostgreSQL container is stopped, credentials are wrong, or the configured database does not exist, startup fails before the API server is launched.

## How to Run the Application

### Option 1: Run with Docker Compose

Before starting FastAPI with Docker Compose, start and verify the standalone PostgreSQL container using the commands above. Because the FastAPI container must connect back to PostgreSQL through the Docker host, set `DB_HOST` and `TEST_DB_HOST` to `host.docker.internal` in `.env` for Docker Compose runs.

Then run Docker Compose for the application container:

```bash
docker compose up --build
```

The application container logs show each startup stage:

1. Validate the configured PostgreSQL connection
2. Run pytest test cases
3. Display the pytest summary
4. Start the API server only if tests pass

If the database connection fails or any test fails, the failure report remains visible in the logs and the FastAPI application is not started. Fix the database configuration, database state, failing test, or application code, then start the workflow again.

Once the tests pass and the app starts, open:

- http://<your-machine-ip>:9000/health
- http://<your-machine-ip>:9000/items
- http://<your-machine-ip>:9000/docs

### Option 2: Run Locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Set the local database environment variables. If the standalone PostgreSQL container is bound to `127.0.0.1:5432`, use `127.0.0.1` as the host:

```bash
export DB_HOST=127.0.0.1
export DB_PORT=5432
export DB_NAME=app_db
export TEST_DB_HOST=127.0.0.1
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
