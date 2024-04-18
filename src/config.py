import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("POSTGRES_NAME", default="postgres")
DB_USERNAME = os.getenv("POSTGRES_USER", default="postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="postgres")
DB_HOST = os.getenv("POSTGRES_HOST", default="localhost")
DB_PORT = os.getenv("POSTGRES_PORT", default=5432)

WEB_HOST = os.getenv("WEB_HOST", default="0.0.0.0")
WEB_PORT = os.getenv("WEB_PORT", default=8080)
