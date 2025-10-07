# School Management System - FastAPI Backend

## Prerequisites
- Python 3.11+

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the API
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Health check: `GET http://localhost:8000/health`
- OpenAPI docs: `http://localhost:8000/docs`

## Database
- Using SQLite (async) by default at `./school.db`.
- Configure via `.env`:
```
database_url=sqlite+aiosqlite:///./school.db
```

Tables are auto-created on startup.

## Seed sample data
```bash
python -m app.db.seed
```

## API Surface
- Students: `/api/v1/students`
- Teachers: `/api/v1/teachers`
- Courses: `/api/v1/courses`
- Sections: `/api/v1/sections`
- Enrollments: `/api/v1/enrollments`
- Attendance: `/api/v1/attendance`
- Grades: `/api/v1/grades`
