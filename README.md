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
├── Dockerfile
├── docker-compose.yml
└── README.md
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
