<?php
declare(strict_types=1);

function get_pdo(): PDO {
	static $pdo = null;
	if ($pdo instanceof PDO) {
		return $pdo;
	}
	$config = require __DIR__ . '/../config.php';
	$dsn = sprintf(
		'mysql:host=%s;port=%s;dbname=%s;charset=%s',
		$config['DB_HOST'],
		$config['DB_PORT'],
		$config['DB_NAME'],
		$config['DB_CHARSET']
	);
	$options = [
		PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
		PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
		PDO::ATTR_EMULATE_PREPARES => false,
	];
	$pdo = new PDO($dsn, $config['DB_USER'], $config['DB_PASS'], $options);
	return $pdo;
}

function send_json(mixed $data, int $statusCode = 200): void {
	header('Content-Type: application/json');
	http_response_code($statusCode);
	echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
	exit;
}

function parse_json_body(): array {
	$raw = file_get_contents('php://input');
	if ($raw === false || $raw === '') {
		return [];
	}
	$parsed = json_decode($raw, true);
	if (json_last_error() !== JSON_ERROR_NONE) {
		send_json(['error' => 'Invalid JSON body'], 400);
	}
	return is_array($parsed) ? $parsed : [];
}

function get_path(): string {
	$uri = $_SERVER['REQUEST_URI'] ?? '/';
	$path = parse_url($uri, PHP_URL_PATH);
	return rtrim($path ?: '/', '/');
}

function require_params(array $data, array $required): void {
	$missing = [];
	foreach ($required as $key) {
		if (!array_key_exists($key, $data) || $data[$key] === '' || $data[$key] === null) {
			$missing[] = $key;
		}
	}
	if ($missing) {
		send_json(['error' => 'Missing required fields', 'fields' => $missing], 400);
	}
}