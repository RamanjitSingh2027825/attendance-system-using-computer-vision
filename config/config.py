import os
from loguru import logger

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
STORAGE_BUCKET = os.getenv("STORAGE_BUCKET")
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

STUDENTS_DATA = os.getenv("STUDENTS_DATA")
STUDENTS_IMAGE_DIR = os.getenv("STUDENTS_IMAGE_DIR")
STUDENTS_ENCODING_FILE = os.getenv("STUDENTS_ENCODING_FILE")