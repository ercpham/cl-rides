"""Implements all the preprocessing functionality for the data.
"""

from cfg.config import *
import pandas as pd
from sqlite3 import Timestamp


def sync_to_last_assignments(drivers_df: pd.DataFrame, riders_df: pd.DataFrame, out: pd.DataFrame) -> pd.DataFrame:
    """Synchronize driver stats to reflect the precalculated assignments. Preassigned riders will be removed from `rf`.

    If synchronization is not possible with the given drivers, the output will be adjusted to match driver availability.
    PRECONDITION: add_temporaries must have been called on drivers_df.
    """
    synced_out = pd.DataFrame()
    d_idx = None
    valid = False
    for idx in out.index:
        phone = out.at[idx, OUTPUT_DRIVER_PHONE_HDR]
        if phone != '':
            # Found new driver phone
            d_idx = drivers_df[drivers_df[DRIVER_PHONE_HDR] == phone].first_valid_index()
            valid = d_idx is not None

        if valid:
            # update driver stats, remove rider from form, transfer to synced dataframe
            drivers_df.at[d_idx, DRIVER_OPENINGS_HDR] -= 1
            entry = out.iloc[[idx]]
            rider_loc = LOC_MAP.get(entry.at[entry.index[0], RIDER_LOCATION_HDR], LOC_MAP[ELSEWHERE])
            drivers_df.at[d_idx, DRIVER_ROUTE_HDR] |= rider_loc
            riders_df.drop(riders_df[riders_df[RIDER_PHONE_HDR] == entry.at[entry.index[0], RIDER_PHONE_HDR]].index, inplace=True)
            synced_out = pd.concat([synced_out, entry])

    return synced_out


def get_prev_driver_phones(prev_out: pd.DataFrame) -> set:
    """Returns all the phone numbers of the drivers from the previous grouping.
    """
    phone_nums = set()
    for phone in prev_out[OUTPUT_DRIVER_PHONE_HDR]:
        phone_nums.add(phone)
    return phone_nums


def rotate_drivers(drivers_df: pd.DataFrame, driver_nums: set):
    """Updates the driver's last driven date and rotates them accordingly.
    """
    for idx in drivers_df.index:
        if drivers_df.at[idx, DRIVER_PHONE_HDR] in driver_nums:
            drivers_df.at[idx, DRIVER_TIMESTAMP_HDR] = Timestamp.now()
    drivers_df.sort_values(by=DRIVER_TIMESTAMP_HDR, inplace=True)


def clean_data(drivers_df: pd.DataFrame, riders_df: pd.DataFrame):
    """Filters out the unneeded columns and and validates the data before assigning.
    """
    _validate_data(drivers_df, riders_df)
    _filter_data(drivers_df, riders_df)


def standardize_permanent_responses(riders_df: pd.DataFrame):
    """Standardize the permanent responses for Friday and Sunday rides.
    """
    for idx in riders_df.index:
        response = riders_df.at[idx, PERMANENT_RIDER_FRIDAY_HDR]
        riders_df.at[idx, PERMANENT_RIDER_FRIDAY_HDR] = RIDE_THERE_KEYWORD if PERMANENT_RIDE_THERE_KEYWORD in response.lower() else ''
        response = riders_df.at[idx, PERMANENT_RIDER_SUNDAY_HDR]
        riders_df.at[idx, PERMANENT_RIDER_SUNDAY_HDR] = RIDE_THERE_KEYWORD if PERMANENT_RIDE_THERE_KEYWORD in response.lower() else ''


def standardize_weekly_responses(riders_df: pd.DataFrame):
    """Standardize the weekly responses for Friday and Sunday rides.
    """
    for idx in riders_df.index:
        response = riders_df.at[idx, WEEKLY_RIDER_FRIDAY_HDR]
        riders_df.at[idx, WEEKLY_RIDER_FRIDAY_HDR] = RIDE_THERE_KEYWORD if WEEKLY_RIDE_THERE_KEYWORD in response.lower() else ''
        response = riders_df.at[idx, WEEKLY_RIDER_SUNDAY_HDR]
        riders_df.at[idx, WEEKLY_RIDER_SUNDAY_HDR] = RIDE_THERE_KEYWORD if WEEKLY_RIDE_THERE_KEYWORD in response.lower() else ''


def filter_friday(riders_df: pd.DataFrame) -> pd.DataFrame:
    """Filters riders that will attend Friday College Life.
    """
    return riders_df.copy()[riders_df[RIDER_FRIDAY_HDR] == RIDE_THERE_KEYWORD]


def filter_sunday(riders_df: pd.DataFrame) -> pd.DataFrame:
    """Filters riders that will attend Sunday service.
    """
    return riders_df.copy()[riders_df[RIDER_SUNDAY_HDR] == RIDE_THERE_KEYWORD]


def prep_necessary_drivers(drivers_df: pd.DataFrame, cnt_riders: int) -> pd.DataFrame:
    driver_cnt = _find_driver_cnt(drivers_df, cnt_riders)
    drivers = drivers_df.copy()[:driver_cnt]
    drivers.sort_values(by=DRIVER_CAPACITY_HDR, ascending=False, inplace=True)
    _add_temporaries(drivers)
    return drivers


def _add_temporaries(drivers_df: pd.DataFrame):
    """Adds temporary columns to the dataframes for calculating assignments.
    """
    drivers_df[DRIVER_OPENINGS_HDR] = drivers_df[DRIVER_CAPACITY_HDR]
    drivers_df[DRIVER_ROUTE_HDR] = LOC_NONE


def _find_driver_cnt(drivers_df: pd.DataFrame, cnt_riders: int) -> int:
    """Determines how many drivers are needed to give rides to all the riders.
    """
    for cnt, idx in enumerate(drivers_df.index):
        if cnt_riders > 0:
            cnt_riders -= drivers_df.at[idx, DRIVER_CAPACITY_HDR]
        else:
            break
    return cnt


def _filter_data(drivers_df: pd.DataFrame, riders_df: pd.DataFrame):
    _filter_drivers(drivers_df)
    _filter_riders(riders_df)


def _filter_drivers(drivers_df: pd.DataFrame):
    remove = drivers_df[drivers_df[DRIVER_PHONE_HDR].isin(IGNORED_DRIVERS)]
    drivers_df.drop(remove.index, inplace=True)


def _filter_riders(riders_df: pd.DataFrame):
    riders_df.drop(columns=[RIDER_TIMESTAMP_HDR], inplace=True)
    remove = riders_df[riders_df[RIDER_PHONE_HDR].isin(IGNORED_RIDERS)]
    riders_df.drop(remove.index, inplace=True)


def _validate_data(drivers_df: pd.DataFrame, riders_df: pd.DataFrame):
    """Recovers proper datatypes and removes duplicates
    """
    _validate_drivers(drivers_df)
    _validate_riders(riders_df)


def _validate_drivers(drivers_df: pd.DataFrame):
    """Enforces datetime datatype on the timestamp and drops duplicates from the drivers list.

    Enforcing the datetime datatype allows us to order the drivers when rewriting them to the sheet to implement cycling.
    """
    drivers_df.drop(drivers_df[ drivers_df[DRIVER_PHONE_HDR] == '' ].index, inplace=True)
    drivers_df.drop_duplicates(subset=DRIVER_PHONE_HDR, inplace=True, keep='last')
    drivers_df[DRIVER_TIMESTAMP_HDR] = pd.to_datetime(drivers_df[DRIVER_TIMESTAMP_HDR])
    drivers_df[DRIVER_CAPACITY_HDR] = drivers_df[DRIVER_CAPACITY_HDR].astype(int)
    drivers_df[DRIVER_PHONE_HDR] = drivers_df[DRIVER_PHONE_HDR].astype(str)


def _validate_riders(riders_df: pd.DataFrame):
    """Drops the oldest duplicates from the riders list.
    """
    riders_df.drop(riders_df[ riders_df[RIDER_PHONE_HDR] == '' ].index, inplace=True)
    riders_df[RIDER_TIMESTAMP_HDR] = pd.to_datetime(riders_df[RIDER_TIMESTAMP_HDR])
    riders_df.sort_values(by=RIDER_TIMESTAMP_HDR, inplace=True)
    riders_df.drop_duplicates(subset=RIDER_PHONE_HDR, inplace=True, keep='last')