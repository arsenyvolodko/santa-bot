import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(name='service logger')

MY_TG_ID = 506954303

BOT_DIR = Path(__file__).parent
WORK_DIR = BOT_DIR.parent

load_dotenv(WORK_DIR / ".env")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DATABASE_URL = os.environ.get("DATABASE_URL")
