-- Schema for Sol Plaatje University Student Record Management System

CREATE DATABASE IF NOT EXISTS student_records CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE student_records;

CREATE TABLE IF NOT EXISTS programmes (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL UNIQUE,
	duration_years INT NOT NULL CHECK (duration_years > 0),
	duration_semesters INT NOT NULL CHECK (duration_semesters > 0),
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS modules (
	id INT AUTO_INCREMENT PRIMARY KEY,
	programme_id INT NOT NULL,
	code VARCHAR(20) NOT NULL,
	name VARCHAR(255) NOT NULL,
	description TEXT NULL,
	credit_hours INT NOT NULL CHECK (credit_hours > 0),
	semester INT NOT NULL CHECK (semester >= 1),
	UNIQUE KEY uniq_programme_code (programme_id, code),
	INDEX idx_programme_semester (programme_id, semester),
	CONSTRAINT fk_modules_programme FOREIGN KEY (programme_id)
		REFERENCES programmes(id) ON DELETE CASCADE,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS students (
	id INT AUTO_INCREMENT PRIMARY KEY,
	student_number VARCHAR(50) NOT NULL UNIQUE,
	full_name VARCHAR(255) NOT NULL,
	programme_id INT NOT NULL,
	year_of_enrollment INT NOT NULL,
	CONSTRAINT fk_students_programme FOREIGN KEY (programme_id)
		REFERENCES programmes(id) ON DELETE RESTRICT,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS enrollments (
	id INT AUTO_INCREMENT PRIMARY KEY,
	student_id INT NOT NULL,
	module_id INT NOT NULL,
	academic_year INT NOT NULL,
	semester INT NOT NULL,
	mark DECIMAL(5,2) NULL,
	UNIQUE KEY uniq_enrollment (student_id, module_id, academic_year, semester),
	INDEX idx_enrollment_student (student_id, academic_year, semester),
	CONSTRAINT fk_enrollments_student FOREIGN KEY (student_id)
		REFERENCES students(id) ON DELETE CASCADE,
	CONSTRAINT fk_enrollments_module FOREIGN KEY (module_id)
		REFERENCES modules(id) ON DELETE CASCADE,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;