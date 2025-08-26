## Student Record Management System (Sol Plaatje University)

Minimal PHP + MySQL API to manage programmes, modules, students, enrollments, and reports.

### 1) Database Setup

- Ensure MySQL is running and you have a user with privileges.
- Import the schema:

```bash
mysql -u root -p < schema.sql
```

Environment variables (optional) for DB connection:
- `DB_HOST` (default: 127.0.0.1)
- `DB_PORT` (default: 3306)
- `DB_NAME` (default: student_records)
- `DB_USER` (default: root)
- `DB_PASS` (default: empty)

### 2) Run the API

Use PHP built-in server:

```bash
php -S 0.0.0.0:8000 -t public
```

### 3) Endpoints

All bodies are JSON. Responses are JSON.

- POST `/programmes`
  - body: `{ "name": "BSc Computer Science", "duration_years": 3, "duration_semesters": 6 }`
- GET `/programmes`

- POST `/modules`
  - body: `{ "programme_id": 1, "code": "CSC101", "name": "Intro to CS", "description": "...", "credit_hours": 16, "semester": 1 }`
- GET `/modules?programme_id=1`

- POST `/students`
  - body: `{ "student_number": "SPU12345", "full_name": "Jane Doe", "programme_id": 1, "year_of_enrollment": 2025 }`
- GET `/students?student_number=SPU12345`

- POST `/enrollments`
  - body: `{ "student_number": "SPU12345", "module_id": 2, "academic_year": 2025, "semester": 1, "mark": 73 }`

- POST `/marks`
  - body: `{ "student_number": "SPU12345", "module_id": 2, "academic_year": 2025, "semester": 1, "mark": 78 }`

- GET `/reports/semester?student_number=SPU12345&academic_year=2025&semester=1`
- GET `/reports/academic-year?student_number=SPU12345&academic_year=2025`
- GET `/reports/transcript?student_number=SPU12345`

### 4) Notes

- Modules are tied to a programme via `programme_id` and store the semester they are offered.
- Enrollments are unique per student/module/year/semester and include the mark.
- The API returns HTTP 4xx for validation errors and 404 when records are not found.