import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

def get_path(VARIABLE_NAME):

    path = os.getenv (VARIABLE_NAME)
    return path

INPUT_PATH = BASE_DIR / get_path("INPUT_PATH")

INVALIDS_PATH = BASE_DIR / get_path ("INVALIDS_PATH")
VALIDS_PATH = BASE_DIR / get_path ("VALIDS_PATH")
TRANSFORMED_PATH = BASE_DIR / get_path ("TRANSFORMED_PATH")
SUMMARY_PATH = BASE_DIR / get_path ("SUMMARY_PATH")


