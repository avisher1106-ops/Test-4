CREATE DATABASE IF NOT EXISTS logs_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE logs_db;

CREATE TABLE IF NOT EXISTS logs (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    method VARCHAR(10) NOT NULL,
    route VARCHAR(512) NOT NULL,
    total_results INT UNSIGNED NOT NULL DEFAULT 0,
    client_ip VARCHAR(45) NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    KEY idx_logs_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
