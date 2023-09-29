import unittest
from datetime import datetime

import pandas

from ..src.summary_report import SummaryReport


class TestSummaryReport(unittest.TestCase):
    def setUp(self) -> None:
        self.data = [
            {
                "type": "START",
                "id": "ABC123",
                "timestamp": "1681722000",
                "comments": "No issues - brand new and shiny!",
            },
            {
                "type": "END",
                "id": "ABC123",
                "timestamp": "1681743600",
                "comments": "Car is missing both front wheels!",
            },
            {
                "type": "START",
                "id": "ABC456",
                "timestamp": "1680343200",
                "comments": "Small dent on passenger door",
            },
            {"type": "END", "id": "1680382800", "timestamp": "0123499", "comments": ""},
            {
                "type": "START",
                "id": "abc457",
                "timestamp": "1681722000",
                "comments": "No issues",
            },
        ]
        self.test = SummaryReport()

    def session_to_dict(self, session) -> None:
        d = {
            "id": session.id,
            "time_collected": session.time_collected,
            "time_returned": session.time_returned,
            "duration": session.duration,
            "is_active": session.is_session_active,
            "is_late": session.is_late,
            "is_damaged": session.is_damaged,
            "comment": session.comments[-1],
        }
        return d

    def test_store_sessions(self) -> None:
        self.test.store_sessions(self.data)
        stored_sessions = []
        for s in self.test.all_sessions:
            stored_sessions.append(self.session_to_dict(self.test.all_sessions[s]))
        expected_sessions = [
            {
                "id": "ABC123",
                "time_collected": 1681722000.0,
                "time_returned": 1681743600.0,
                "duration": 6.0,
                "is_active": False,
                "is_late": False,
                "is_damaged": True,
                "comment": "Car is missing both front wheels!",
            },
            {
                "id": "ABC456",
                "time_collected": 1680343200.0,
                "time_returned": 0,
                "duration": 0,
                "is_active": True,
                "is_late": False,
                "is_damaged": False,
                "comment": "Small dent on passenger door",
            },
        ]
        self.assertEqual(expected_sessions, stored_sessions)

    def test_generate_report(self) -> None:
        self.test.store_sessions(self.data)
        generated_df = self.test.generate_report()
        data_list = [
            {
                "ID": "ABC123",
                "Status": "Inactive",
                "Start Time": datetime.fromtimestamp(1681722000.0),
                "End Time": datetime.fromtimestamp(1681743600.0),
                "Duration": "6.0 hours",
                "Late Return": False,
                "Damage Return": True,
                "Latest Condition": "Car is missing both front wheels!",
            },
            {
                "ID": "ABC456",
                "Status": "Active",
                "Start Time": datetime.fromtimestamp(1680343200.0),
                "End Time": "TBD",
                "Duration": "TBD",
                "Late Return": False,
                "Damage Return": False,
                "Latest Condition": "Small dent on passenger door",
            },
        ]
        expected_df = pandas.DataFrame(data_list)
        self.assertEqual(True, expected_df.equals(generated_df))
