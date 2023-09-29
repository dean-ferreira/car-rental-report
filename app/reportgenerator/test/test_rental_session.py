import datetime
import unittest

from ..src.rental_session import RentalSession


class TestRentalSession(unittest.TestCase):
    def setUp(self) -> None:
        self.session = RentalSession()
        self.time_session = RentalSession(_collected=1681722000, _returned=1681743600)

    def test_start_session(self):
        valid_id = "ABC123"
        valid_timestamp = 1681722000
        valid_comment = "No issues - brand new and shiny!"
        self.assertEqual(
            True, self.session.start_session(valid_id, valid_timestamp, valid_comment)
        )

        invalid_valid_id = "1680382800"
        invalid_valid_timestamp = 123499
        invalid_valid_comment = ""
        self.assertEqual(
            False,
            self.session.start_session(
                invalid_valid_id, invalid_valid_timestamp, invalid_valid_comment
            ),
        )

    def test_end_session(self):
        started_session = RentalSession()
        started_session.start_session(
            _id="ABC123",
            _time_collected=1681722000,
            _comment="No issues - brand new and shiny!",
        )
        started_session.end_session(
            _time_returned=1681743600, _comment="Car is missing both front wheels!"
        )
        self.assertEqual(1681743600.0, started_session.time_returned)
        self.assertEqual(6.0, started_session.duration)
        self.assertEqual(False, started_session.is_late)
        self.assertEqual(True, started_session.is_damaged)
        self.assertEqual(False, started_session.is_session_active)

    def test_set_session_id(self):
        self.assertEqual(True, self.session.set_session_id("ABC123"))
        self.assertEqual(False, self.session.set_session_id("abc123"))
        self.assertEqual(False, self.session.set_session_id("123ABC"))
        self.assertEqual(False, self.session.set_session_id("1680382800"))

    def test_set_time_collected(self):
        self.assertEqual(True, self.session.set_time_collected("1681722000"))
        self.assertEqual(True, self.session.set_time_collected(1681722000))
        self.assertEqual(True, self.session.set_time_collected("0123499"))

    def test_set_time_returned(self):
        self.assertEqual(True, self.session.set_time_returned("1681722000"))
        self.assertEqual(True, self.session.set_time_returned(1681722000))
        self.assertEqual(True, self.session.set_time_returned("0123499"))

    def test_set_initial_comment(self):
        self.assertEqual(
            True, self.session.set_initial_comment("No issues - brand new and shiny!")
        )
        self.assertEqual(False, self.session.set_initial_comment(""))

    def test_calculate_session_duration(self):
        self.assertEqual(
            6.0,
            self.time_session.calculate_session_duration(
                self.time_session.time_collected, self.time_session.time_returned
            ),
        )

    def test_set_session_duration(self):
        self.time_session.set_session_duration()
        self.assertEqual(6.0, self.time_session.duration)

    def test_set_late_status(self):
        self.time_session.set_session_duration()
        self.time_session.set_late_status(self.time_session.duration)
        self.assertEqual(False, self.time_session.is_late)

    def test_set_damage_status(self):
        self.session.set_damage_status("Damaged")
        self.assertEqual(True, self.session.is_damaged)
        self.time_session.set_damage_status("")
        self.assertEqual(False, self.time_session.is_damaged)

    def test_generate_summary(self):
        complete_session = RentalSession(
            _id="ABC123",
            _collected=1681722000,
            _returned=1681743600,
            _duration=6.0,
            _active=False,
            _late=False,
            _damage=True,
        )
        complete_session.set_damage_status("Car is missing both front wheels!")
        generated_summary = complete_session.generate_summary()
        expected_summary = {
            "ID": "ABC123",
            "Status": "Inactive",
            "Start Time": datetime.datetime.fromtimestamp(1681722000),
            "End Time": datetime.datetime.fromtimestamp(1681743600),
            "Duration": "6.0 hours",
            "Late Return": False,
            "Damage Return": True,
            "Latest Condition": "Car is missing both front wheels!",
        }
        self.assertEqual(expected_summary, generated_summary)
