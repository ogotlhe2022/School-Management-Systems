<?php
declare(strict_types=1);

require __DIR__ . '/../src/db.php';

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$path = get_path();

try {
	switch ([$method, $path]) {
		// Programmes
		case ['POST', '/programmes']:
			createProgramme();
			break;
		case ['GET', '/programmes']:
			listProgrammes();
			break;

		// Modules
		case ['POST', '/modules']:
			createModule();
			break;
		case ['GET', '/modules']:
			listModules();
			break;

		// Students
		case ['POST', '/students']:
			createStudent();
			break;
		case ['GET', '/students']:
			getStudent();
			break;

		// Enrollments and marks
		case ['POST', '/enrollments']:
			createEnrollment();
			break;
		case ['POST', '/marks']:
			setMark();
			break;

		// Reports
		case ['GET', '/reports/semester']:
			reportSemester();
			break;
		case ['GET', '/reports/academic-year']:
			reportAcademicYear();
			break;
		case ['GET', '/reports/transcript']:
			reportTranscript();
			break;

		default:
			send_json(['error' => 'Not Found'], 404);
	}
} catch (Throwable $e) {
	send_json(['error' => 'Server Error', 'message' => $e->getMessage()], 500);
}

// Handlers

function createProgramme(): void {
	$body = parse_json_body();
	require_params($body, ['name', 'duration_years', 'duration_semesters']);
	$pdo = get_pdo();
	$sql = 'INSERT INTO programmes (name, duration_years, duration_semesters) VALUES (:name, :dy, :ds)';
	$stmt = $pdo->prepare($sql);
	$stmt->execute([
		':name' => $body['name'],
		':dy' => (int)$body['duration_years'],
		':ds' => (int)$body['duration_semesters'],
	]);
	send_json(['id' => (int)$pdo->lastInsertId()]);
}

function listProgrammes(): void {
	$pdo = get_pdo();
	$rows = $pdo->query('SELECT id, name, duration_years, duration_semesters FROM programmes ORDER BY name')->fetchAll();
	send_json($rows);
}

function createModule(): void {
	$body = parse_json_body();
	require_params($body, ['programme_id', 'code', 'name', 'credit_hours', 'semester']);
	$pdo = get_pdo();
	$sql = 'INSERT INTO modules (programme_id, code, name, description, credit_hours, semester) VALUES (:pid, :code, :name, :desc, :ch, :sem)';
	$stmt = $pdo->prepare($sql);
	$stmt->execute([
		':pid' => (int)$body['programme_id'],
		':code' => $body['code'],
		':name' => $body['name'],
		':desc' => $body['description'] ?? null,
		':ch' => (int)$body['credit_hours'],
		':sem' => (int)$body['semester'],
	]);
	send_json(['id' => (int)$pdo->lastInsertId()]);
}

function listModules(): void {
	$pdo = get_pdo();
	$programmeId = isset($_GET['programme_id']) ? (int)$_GET['programme_id'] : null;
	if ($programmeId) {
		$stmt = $pdo->prepare('SELECT id, programme_id, code, name, description, credit_hours, semester FROM modules WHERE programme_id = :pid ORDER BY semester, code');
		$stmt->execute([':pid' => $programmeId]);
		$rows = $stmt->fetchAll();
	} else {
		$rows = $pdo->query('SELECT id, programme_id, code, name, description, credit_hours, semester FROM modules ORDER BY programme_id, semester, code')->fetchAll();
	}
	send_json($rows);
}

function createStudent(): void {
	$body = parse_json_body();
	require_params($body, ['student_number', 'full_name', 'programme_id', 'year_of_enrollment']);
	$pdo = get_pdo();
	$sql = 'INSERT INTO students (student_number, full_name, programme_id, year_of_enrollment) VALUES (:sn, :name, :pid, :yoe)';
	$stmt = $pdo->prepare($sql);
	$stmt->execute([
		':sn' => $body['student_number'],
		':name' => $body['full_name'],
		':pid' => (int)$body['programme_id'],
		':yoe' => (int)$body['year_of_enrollment'],
	]);
	send_json(['id' => (int)$pdo->lastInsertId()]);
}

function getStudent(): void {
	$pdo = get_pdo();
	if (!isset($_GET['student_number'])) {
		send_json(['error' => 'student_number is required'], 400);
	}
	$stmt = $pdo->prepare('SELECT id, student_number, full_name, programme_id, year_of_enrollment FROM students WHERE student_number = :sn');
	$stmt->execute([':sn' => $_GET['student_number']]);
	$student = $stmt->fetch();
	if (!$student) {
		send_json(['error' => 'Student not found'], 404);
	}
	send_json($student);
}

function resolveStudentId(PDO $pdo, array $body): int {
	if (isset($body['student_id'])) {
		return (int)$body['student_id'];
	}
	if (isset($body['student_number'])) {
		$stmt = $pdo->prepare('SELECT id FROM students WHERE student_number = :sn');
		$stmt->execute([':sn' => $body['student_number']]);
		$row = $stmt->fetch();
		if ($row) {
			return (int)$row['id'];
		}
	}
	send_json(['error' => 'student_id or student_number is required and must exist'], 400);
}

function createEnrollment(): void {
	$body = parse_json_body();
	require_params($body, ['module_id', 'academic_year', 'semester']);
	$pdo = get_pdo();
	$studentId = resolveStudentId($pdo, $body);
	$sql = 'INSERT INTO enrollments (student_id, module_id, academic_year, semester, mark) VALUES (:sid, :mid, :ay, :sem, :mark)';
	$stmt = $pdo->prepare($sql);
	$stmt->execute([
		':sid' => $studentId,
		':mid' => (int)$body['module_id'],
		':ay' => (int)$body['academic_year'],
		':sem' => (int)$body['semester'],
		':mark' => isset($body['mark']) ? (float)$body['mark'] : null,
	]);
	send_json(['id' => (int)$pdo->lastInsertId()]);
}

function setMark(): void {
	$body = parse_json_body();
	require_params($body, ['module_id', 'academic_year', 'semester', 'mark']);
	$pdo = get_pdo();
	$studentId = resolveStudentId($pdo, $body);
	$sql = 'UPDATE enrollments SET mark = :mark WHERE student_id = :sid AND module_id = :mid AND academic_year = :ay AND semester = :sem';
	$stmt = $pdo->prepare($sql);
	$stmt->execute([
		':mark' => (float)$body['mark'],
		':sid' => $studentId,
		':mid' => (int)$body['module_id'],
		':ay' => (int)$body['academic_year'],
		':sem' => (int)$body['semester'],
	]);
	if ($stmt->rowCount() === 0) {
		send_json(['error' => 'Enrollment not found'], 404);
	}
	send_json(['updated' => true]);
}

function reportSemester(): void {
	$pdo = get_pdo();
	$studentNumber = $_GET['student_number'] ?? null;
	$academicYear = isset($_GET['academic_year']) ? (int)$_GET['academic_year'] : null;
	$semester = isset($_GET['semester']) ? (int)$_GET['semester'] : null;
	if (!$studentNumber || !$academicYear || !$semester) {
		send_json(['error' => 'student_number, academic_year, semester are required'], 400);
	}
	$student = fetchStudentByNumber($pdo, $studentNumber);
	$sql = 'SELECT m.code, m.name, m.credit_hours, e.mark
		FROM enrollments e
		JOIN modules m ON m.id = e.module_id
		WHERE e.student_id = :sid AND e.academic_year = :ay AND e.semester = :sem
		ORDER BY m.code';
	$stmt = $pdo->prepare($sql);
	$stmt->execute([':sid' => (int)$student['id'], ':ay' => $academicYear, ':sem' => $semester]);
	$rows = $stmt->fetchAll();
	send_json(['student' => $student, 'academic_year' => $academicYear, 'semester' => $semester, 'results' => $rows]);
}

function reportAcademicYear(): void {
	$pdo = get_pdo();
	$studentNumber = $_GET['student_number'] ?? null;
	$academicYear = isset($_GET['academic_year']) ? (int)$_GET['academic_year'] : null;
	if (!$studentNumber || !$academicYear) {
		send_json(['error' => 'student_number and academic_year are required'], 400);
	}
	$student = fetchStudentByNumber($pdo, $studentNumber);
	$sql = 'SELECT e.semester, m.code, m.name, m.credit_hours, e.mark
		FROM enrollments e
		JOIN modules m ON m.id = e.module_id
		WHERE e.student_id = :sid AND e.academic_year = :ay
		ORDER BY e.semester, m.code';
	$stmt = $pdo->prepare($sql);
	$stmt->execute([':sid' => (int)$student['id'], ':ay' => $academicYear]);
	$rows = $stmt->fetchAll();
	send_json(['student' => $student, 'academic_year' => $academicYear, 'results' => $rows]);
}

function reportTranscript(): void {
	$pdo = get_pdo();
	$studentNumber = $_GET['student_number'] ?? null;
	if (!$studentNumber) {
		send_json(['error' => 'student_number is required'], 400);
	}
	$student = fetchStudentByNumber($pdo, $studentNumber);
	$sql = 'SELECT e.academic_year, e.semester, m.code, m.name, m.credit_hours, e.mark
		FROM enrollments e
		JOIN modules m ON m.id = e.module_id
		WHERE e.student_id = :sid
		ORDER BY e.academic_year, e.semester, m.code';
	$stmt = $pdo->prepare($sql);
	$stmt->execute([':sid' => (int)$student['id']]);
	$rows = $stmt->fetchAll();
	$totalCredits = 0;
	foreach ($rows as $row) {
		$totalCredits += (int)$row['credit_hours'];
	}
	send_json(['student' => $student, 'total_credits' => $totalCredits, 'records' => $rows]);
}

function fetchStudentByNumber(PDO $pdo, string $studentNumber): array {
	$stmt = $pdo->prepare('SELECT s.id, s.student_number, s.full_name, s.year_of_enrollment, p.name AS programme_name
		FROM students s JOIN programmes p ON p.id = s.programme_id WHERE s.student_number = :sn');
	$stmt->execute([':sn' => $studentNumber]);
	$student = $stmt->fetch();
	if (!$student) {
		send_json(['error' => 'Student not found'], 404);
	}
	return $student;
}