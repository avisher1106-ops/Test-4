import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Config:
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "fruity")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "logs_db")

    FRUITYVICE_BASE_URL = os.getenv("FRUITYVICE_BASE_URL", "https://www.fruityvice.com")
    FRUITYVICE_TIMEOUT = float(os.getenv("FRUITYVICE_TIMEOUT", "10"))

    PORT = int(os.getenv("PORT", "4000"))
