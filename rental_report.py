#!/usr/bin/env python3
from json import load
import sys


def read_json_file(file_path: str) -> list:
    data = []
    with open(file_path, "r") as file:
        data = load(file)
    return data


def main():
    events = read_json_file(sys.argv[1])


if __name__ == "__main__":
    main()
