from json import JSONDecodeError, load


def read_json_file(file_path: str) -> list:
    """
    Reads the data from JSON file and stores each object (event) as a dictionary

    Returns:
        list: list of dict
    """
    data = []
    try:
        with open(file_path, "r") as file:
            data = load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except JSONDecodeError as err:
        raise JSONDecodeError(err.msg, err.doc, err.pos)
    else:
        return data
