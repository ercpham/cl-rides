"""Includes all constants used in the project.
"""

### Column headers for the dataframes
OUTPUT_DRIVER_NAME_HDR = 'Driver'
OUTPUT_DRIVER_PHONE_HDR = 'Driver Phone #'
OUTPUT_DRIVER_CAPACITY_HDR = 'Seats'

DRIVER_TIMESTAMP_HDR = 'Timestamp'
DRIVER_NAME_HDR = 'Name'
DRIVER_PHONE_HDR = 'Phone Number'
DRIVER_CAPACITY_HDR = 'Number of Seats in Car (not including you)'

RIDER_TIMESTAMP_HDR = 'Timestamp'
RIDER_NAME_HDR = 'Rider'
RIDER_PHONE_HDR = 'Rider Phone #'
RIDER_LOCATION_HDR = 'Location'
RIDER_FRIDAY_HDR = 'Friday'
RIDER_SUNDAY_HDR = 'Sunday'
RIDER_NOTES_HDR = 'Notes'

PERMANENT_RIDER_TIMESTAMP_HDR = 'Timestamp'
PERMANENT_RIDER_NAME_HDR = 'Full Name:'
PERMANENT_RIDER_PHONE_HDR = 'Phone Number: '
PERMANENT_RIDER_LOCATION_HDR = 'Where should we pick you up?'
PERMANENT_RIDER_FRIDAY_HDR = 'Which service(s) do you need a permanent ride for? [Friday Night Bible Study | 6:30 pm]'
PERMANENT_RIDER_SUNDAY_HDR = 'Which service(s) do you need a permanent ride for? [Sunday Service | 8:30 am/10:45 am]'
PERMANENT_RIDER_NOTES_HDR = 'Other Notes'

WEEKLY_RIDER_TIMESTAMP_HDR = 'Timestamp'
WEEKLY_RIDER_NAME_HDR = 'Full Name'
WEEKLY_RIDER_PHONE_HDR = 'Phone Number '
WEEKLY_RIDER_LOCATION_HDR = 'Where should we pick you up from?'
WEEKLY_RIDER_FRIDAY_HDR = 'Friday Night Bible Study (Friday @7pm) (Rides from Campus will be provided at Peterson Loop at 6:30 pm)'
WEEKLY_RIDER_SUNDAY_HDR = 'Sunday Service '
WEEKLY_RIDER_NOTES_HDR = 'Additional Comments / Questions / Concerns'


### For parsing the responses for attending the Friday/Sunday services
PERMANENT_RIDE_THERE_KEYWORD = 'yes'
WEEKLY_RIDE_THERE_KEYWORD = 'there'
RIDE_THERE_KEYWORD = 'yes'

DRIVER_OPENINGS_HDR = 'Open seats'
DRIVER_ROUTE_HDR = 'Locations'

# File paths
import os
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pickle')
CFG_PATH = os.path.dirname(os.path.realpath(__file__))
MAP_FILE = os.path.join(CFG_PATH, 'map.txt')
IGNORE_DRIVERS_FILE = os.path.join(CFG_PATH, 'ignore_drivers.txt')
IGNORE_RIDERS_FILE = os.path.join(CFG_PATH, 'ignore_riders.txt')
SERVICE_ACCT_FILE = os.path.join(CFG_PATH, 'service_account.json')
SHEET_IDS_FILE = os.path.join(CFG_PATH, 'sheet_ids.json')

# Sheet ID keys
PERMANENT_SHEET_KEY = 'permanent'
WEEKLY_SHEET_KEY = 'weekly'
DRIVER_SHEET_KEY = 'drivers'
OUTPUT_SHEET_KEY = 'out'

# The number of openings required for a car to freely pick up from a neighboring location
GROUPING_THRESHOLD = 'threshold'
GLOBALS = {                     # Use a dict in order to modify the global var later
    GROUPING_THRESHOLD: 2
}

# Route codes
LOC_KEY_ELSEWHERE = 'ELSEWHERE'
LOC_NONE = 0b0
LOC_MAP = {
    LOC_KEY_ELSEWHERE: LOC_NONE
}

# Lists to be filled later
IGNORED_DRIVERS = []
IGNORED_RIDERS = []
