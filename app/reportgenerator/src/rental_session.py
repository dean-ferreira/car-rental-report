import datetime
import re

from ..src.utils import validate_timestamp


class RentalSession:
    def __init__(
        self,
        _id="",
        _collected=0,
        _returned=0,
        _duration=0,
        _active=True,
        _late=False,
        _damage=False,
    ) -> None:
        self.id = _id
        self.time_collected = _collected
        self.time_returned = _returned
        self.duration = _duration
        self.is_session_active = _active
        self.is_late = _late
        self.is_damaged = _damage
        self.comments = []

    def start_session(self, _id, _time_collected, _comment) -> bool:
        """
        Starts a rental session by assigning values retrieved from the START event

        Returns:
            boolean: Indicating if the rental session was started successfully, invalid values will return False
        """
        return (
            self.set_session_id(_id)
            and self.set_time_collected(_time_collected)
            and self.set_initial_comment(_comment)
        )

    def end_session(self, _time_returned, _comment) -> None:
        """
        Ends a rental sessions by assigning values retrieved from the END event
        """
        self.set_time_returned(_time_returned)
        self.set_session_duration()
        self.set_late_status(self.duration)
        self.set_damage_status(_comment)
        self.is_session_active = False

    def set_session_id(self, _id) -> bool:
        """
        Validates the session ID
        """
        if re.match("[A-Z][A-Z][A-Z][0-9][0-9][0-9]", _id):
            self.id = _id
            return True
        else:
            return False

    def set_time_collected(self, _timestamp) -> bool:
        """
        Validates the collected timestamp
        """
        if validate_timestamp(_timestamp) == True:
            self.time_collected = float(_timestamp)
            return True
        else:
            return False

    def set_time_returned(self, _timestamp) -> bool:
        """
        Validates the returned timestamp
        """
        if validate_timestamp(_timestamp) == True:
            self.time_returned = float(_timestamp)
            return True
        else:
            return False

    def set_initial_comment(self, _comment) -> bool:
        """
        Adds a comment when a rental session is started

        Returns:
            boolean: Indicating if the comment is not empty
        """
        if len(_comment) > 0:
            self.comments.append(_comment)
            return True
        else:
            return False

    def calculate_session_duration(self, _collected, _returned) -> float:
        """
        Calculates the duration (in hours) of the rental session
        """
        collected = int(_collected)
        returned = int(_returned)
        return round(abs(returned - collected) / 3600, 2)

    def set_session_duration(self) -> None:
        """
        Sets the rental duration
        """
        self.duration = self.calculate_session_duration(
            self.time_collected, self.time_returned
        )

    def set_late_status(self, _duration) -> None:
        """
        Determines if the car was returned late

        If the rental duration is more than 24 hours; the car is late
        """
        if _duration > 24:
            self.is_late = True
        else:
            self.is_late = False

    def set_damage_status(self, _comment) -> None:
        """
        Determines if the car was returned damaged

        Returns:
            boolean: Returns True if the END event has a non-empty comment
        """
        if len(_comment) > 0:
            self.is_damaged = True
            self.comments.append(_comment)

    def generate_summary(self) -> dict:
        """
        Generates a summary for the RentalSession

        Returns:
            dict: A dict mapping keys to the corresponding rental session data
        """
        summary = {
            "ID": self.id,
            "Status": "Active" if self.is_session_active else "Inactive",
            "Start Time": datetime.datetime.fromtimestamp(self.time_collected),
            "End Time": "TBD"
            if self.time_returned == 0
            else datetime.datetime.fromtimestamp(self.time_returned),
            "Duration": "TBD" if self.duration == 0 else f"{self.duration} hours",
            "Late Return": self.is_late,
            "Damage Return": self.is_damaged,
            "Latest Condition": self.comments[-1],
        }
        return summary
