from datetime import datetime, timezone

import pymysql
from pymysql.cursors import DictCursor

from config import Config

CREATE_DATABASE_SQL = (
    f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` "
    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
)

CREATE_LOGS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS logs (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    method VARCHAR(10) NOT NULL,
    route VARCHAR(512) NOT NULL,
    total_results INT UNSIGNED NOT NULL DEFAULT 0,
    client_ip VARCHAR(45) NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    KEY idx_logs_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
"""


def get_connection(use_database: bool = True):
    return pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME if use_database else None,
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=True,
        connect_timeout=10,
    )


def init_db() -> None:
    server = get_connection(use_database=False)
    try:
        with server.cursor() as cursor:
            cursor.execute(CREATE_DATABASE_SQL)
    finally:
        server.close()

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_LOGS_TABLE_SQL)
    finally:
        connection.close()


def insert_log(method: str, route: str, total_results: int, client_ip: str) -> None:
    created_at = datetime.now(timezone.utc).replace(tzinfo=None)
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO logs (method, route, total_results, client_ip, created_at) "
                "VALUES (%s, %s, %s, %s, %s)",
                (method[:10], route[:512], total_results, client_ip[:45], created_at),
            )
    finally:
        connection.close()
