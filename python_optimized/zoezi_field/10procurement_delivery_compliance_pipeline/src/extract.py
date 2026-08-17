from typing import Any


def find_table(file: Any) -> list[dict]:
    """
        This module uses the helper function to recursively find non_empty
    list of dictionaries in the json file. The purpose of the helper
    function is to avoid logging errors whenever a branch does not have
    list of dictionaries because lack of it does not necessarily mean
    that the extraction failed.
    """

    if isinstance(file, list):
        if file and all(isinstance(record, dict) for record in file):
            return file

        return None

    if isinstance(file, dict):
        for record in file.values():
            table = find_table(record)

            if table is not None:
                return table

    return None


def extract_table(raw_file: Any) -> list[dict]:

    table = find_table(raw_file)

    if table is None:
        raise ValueError("could not find a valid list of dictionary")

    return table


def extract_depot(raw_file: str) -> str:

    if not isinstance(raw_file, dict):
        raise KeyError("json payload must be dictionary")

    depot = raw_file.get("depot")

    if not depot:
        raise KeyError("missing 'depot' key in the file")

    return depot


def extract_batch_id(raw_file: str) -> str:

    if not isinstance(raw_file, dict):
        raise KeyError("json payload must be a dictionary")

    batch_id = raw_file.get("batch_id")

    if not batch_id:
        raise KeyError("'depot' key not found in metadata")

    return batch_id
