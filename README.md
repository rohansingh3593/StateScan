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

This will start both the FastAPI app and the PostgreSQL database.

Once running, open:

- http://localhost:9000/health
- http://localhost:9000/items
- http://localhost:9000/docs

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
curl -X POST "http://localhost:9000/items" -H "Content-Type: application/json" -d '{"name":"sample item"}'
```

### List items

```bash
curl "http://localhost:9000/items"
```
