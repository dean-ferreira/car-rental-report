#!/usr/bin/env python3
import datetime
import sys

from app.reportgenerator.src.summary_report import SummaryReport
from app.reportgenerator.src.utils import read_json_file


def main():
    events = read_json_file(sys.argv[1])
    summary_report = SummaryReport()
    summary_report.store_sessions(events)
    generated_report = summary_report.generate_report()
    generated_report.to_csv(f"SR_{datetime.date.today()}.csv")


if __name__ == "__main__":
    main()
