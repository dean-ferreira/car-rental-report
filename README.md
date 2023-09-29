# car-rental-report

### About the Project

This Python application will parse a JSON file and generate a summary report for all rental sessions. The report will print to console and be saved as a file.

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
