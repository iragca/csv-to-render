import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

APP_CONFIG = PROJECT_ROOT / "src" / "config.py"

DATA_PATH = PROJECT_ROOT / "data"

logger.info(f"Project root: {PROJECT_ROOT}")
logger.info(f"App config path: {APP_CONFIG}")

# Check if .env file exists and load it
if not (PROJECT_ROOT / ".env").exists():
    logger.error("No .env file found in the project root.")

# Check if DATABASE_URL is set in the environment variables
if DATABASE_URL is None:
    logger.error("DATABASE_URL wasn't found in the environment variables.")