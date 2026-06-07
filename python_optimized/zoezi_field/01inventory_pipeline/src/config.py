import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_VAR = BASE_DIR / ".env"
load_dotenv (ENV_VAR)
def get_env(VARIABLE_NAME):
    path = os.getenv (VARIABLE_NAME)

    if not path:
        raise ValueError(f"the variable {VARIABLE_NAME} is not found")
    
    return path

INPUT_PATH = BASE_DIR / get_env("INPUT_PATH")