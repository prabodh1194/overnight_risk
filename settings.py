import logging
import os

import dotenv

logger = logging.getLogger(__name__)

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
