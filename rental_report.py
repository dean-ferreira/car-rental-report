#!/usr/bin/env python3
from json import load
import sys

from app.reportgenerator.src.utils import read_json_file


def main():
    events = read_json_file(sys.argv[1])
    print(events)


if __name__ == "__main__":
    main()
