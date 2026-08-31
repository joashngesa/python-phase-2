def extract_table(raw_file):

    if not isinstance(raw_file, list):
        raise TypeError(f"{raw_file} is not a list")
