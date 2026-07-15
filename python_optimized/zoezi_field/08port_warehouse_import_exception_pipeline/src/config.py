import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_VAR = BASE_DIR / ".env.config"

load_dotenv(ENV_VAR)


def get_env_variable(VARIABLE_NAME):
    """
    used to retrieve the environment variables saved in .env.config
    """
    var_name = os.getenv(VARIABLE_NAME)

    if var_name is None or var_name.strip() == "":
        raise ValueError(
            f"⁉️ the variable {VARIABLE_NAME} is not found in .env.config ⚠️"
        )

    return var_name


INPUT_DIR = BASE_DIR / get_env_variable("INPUT_DIR")

VALID_DIR = BASE_DIR / get_env_variable("VALID_DIR")
INVALID_DIR = BASE_DIR / get_env_variable("INVALID_DIR")
QUARANTINE_DIR = BASE_DIR / get_env_variable("QUARANTINE_DIR")
FILE_SUMMARY_DIR = BASE_DIR / get_env_variable("FILE_SUMMARY_DIR")
RUN_SUMMARY_DIR = BASE_DIR / get_env_variable("RUN_SUMMARY_DIR")
TRANSFORMED_DIR = BASE_DIR / get_env_variable("TRANSFORMED_DIR")

FILE_PATTERN = get_env_variable("FILE_PATTERN")
