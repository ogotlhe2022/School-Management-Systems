<?php
declare(strict_types=1);

return [
	'DB_HOST' => getenv('DB_HOST') !== false ? getenv('DB_HOST') : '127.0.0.1',
	'DB_PORT' => getenv('DB_PORT') !== false ? getenv('DB_PORT') : '3306',
	'DB_NAME' => getenv('DB_NAME') !== false ? getenv('DB_NAME') : 'student_records',
	'DB_USER' => getenv('DB_USER') !== false ? getenv('DB_USER') : 'root',
	'DB_PASS' => getenv('DB_PASS') !== false ? getenv('DB_PASS') : '',
	'DB_CHARSET' => 'utf8mb4',
];