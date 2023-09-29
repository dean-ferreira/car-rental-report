# car-rental-report

## About the Project

![example](images/example_output.png?raw=true)
This Python application will parse a JSON file and generate a summary report for all rental sessions. The report will be saved as a csv file named SR_YYYY-MM-DD.csv

The summary report contains the following fields for each rental session:

- ID
- Status
  - (Active/Inactive)
  - Active sessions will be those without an END event
- Start Time
- End Time
- Duration
- Late Return
  - A boolean flag indicating if the car was returned later than expected
  - Should be true if the session was longer than 24 hours
- Damage Return
  - A boolean flag indicating if the car was damaged upon return
  - Should be true if comments is not an empty string for the END event
- Latest Condition
  - Comment describing the condition of the vehicle

## Built With

- Python
- Pandas

## Getting Started

### Prerequisites

- Python

  - Via installer: https://www.python.org/downloads/

- Pandas
  ```sh
  pip install pandas
  ```

### Installation

1. Clone the repo
   ```sh
    git clone https://github.com/dean-ferreira/car-rental-report.git
   ```
2. Execute this application using the following syntax:

   ```sh
   python rental_report.py json_file
   ```

   where json_file represents the file path to the JSON file

## Extra

### Assumptions

- A valid event contains valid values for all fields
  - Exception for "END" events; comments can be an empty string
  - Invalid events are not stored
- A valid rental session ID is the format "XXX000"
  - X represents a capital alphabetic character (A-Z)
  - 0 represents a digit (0-9)
- Timestamp must be a valid UNIX epoch timestamp

### Comments

- Future Iterations
  - Improve generating the summary report, currently a summary for each rental session is generated everytime a summary report is generated. Should only generate (new) rental summaries that were not included since the previous summary report.
  - Improve how invalid data is handled, currently invalid data is just ignored.
