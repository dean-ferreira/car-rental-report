from datetime import datetime

import pandas

from ..src.rental_session import RentalSession


class SummaryReport:
    def __init__(self) -> None:
        self.all_sessions = (
            {}
        )  # Store each RentalSession object where they key is the ID
        self.all_summaries = (
            []
        )  # Store each RentalSession generated summary (list of dict)
        self.num_active_sessions = 0
        self.num_inactive_sessions = 0

    def store_sessions(self, data: dict) -> None:
        """
        Creates/Modifies RentalSession objects for each event.
        """
        for event in data:
            if event == {}:
                return
            if event["type"] == "START":
                new_session = RentalSession()
                if (
                    new_session.start_session(
                        _id=event["id"],
                        _time_collected=event["timestamp"],
                        _comment=event["comments"],
                    )
                ) == False:
                    continue
                else:
                    self.all_sessions[event["id"]] = new_session
                    self.num_active_sessions += 1
            elif event["type"] == "END":
                if event["id"] not in self.all_sessions:
                    continue
                else:
                    session = self.all_sessions[event["id"]]
                    session.end_session(
                        _time_returned=event["timestamp"], _comment=event["comments"]
                    )
                    self.num_active_sessions -= 1
                    self.num_inactive_sessions += 1

    def generate_report(self) -> pandas.DataFrame:
        """
        Generates the summary report for all rental sessions
        """
        for session in self.all_sessions:
            self.all_summaries.append(self.all_sessions[session].generate_summary())
        data_frame = pandas.DataFrame(self.all_summaries)
        return data_frame
