"""Implements usage of the Google Sheets API, including reading driver/rider data and writing to the output sheet.
"""

from cfg.config import *
import gspread
import json
import lib.preprocessing as prep
import os
import pandas as pd
import pickle
from typing import Tuple
import logging


def update_pickles():
    """Pull riders and drivers from the Google Sheets and write to the pickle files.
    """
    # connect Google Sheets
    gc = gspread.service_account(filename=SERVICE_ACCT_FILE)

    with open(os.path.join(CFG_PATH, SHEET_IDS_FILE)) as gid_json:
        gid_data = json.load(gid_json)

    for key in gid_data:
        logging.info(f'Downloading {key}')
        ws = gc.open_by_key(gid_data[key]).get_worksheet(0)
        records = ws.get_all_records()
        with open(os.path.join(DATA_PATH, key), 'wb') as pickle_file:
            pickle.dump(records, pickle_file)


def print_pickles():
    """Print the riders and drivers in the pickle files.

    There is no call to the Google Sheets API, so the printed data is from the last call to update_pickles.
    """
    with open(os.path.join(CFG_PATH, SHEET_IDS_FILE)) as gid_json:
        keys = json.load(gid_json).keys()

    for key in keys:
        with open(os.path.join(DATA_PATH, key), 'rb') as pickle_file:
            records = pickle.load(pickle_file)
            df = pd.DataFrame(records)
            logging.debug(f'Printing {key}\n{df}')


def get_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return a tuple of pandas DataFrames, ordered as (permanent riders, weekly riders, drivers)

    Updates rides data on call. Use get_cached_data() to get prefetched data.
    """
    update_pickles()
    return get_cached_input()


def get_cached_input() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return a tuple of pandas DataFrames, ordered as (drivers, riders)
    
    If the rides data has not been read previously, the results may be outdated or an error might occur.
    """
    with open(os.path.join(DATA_PATH, PERMANENT_SHEET_KEY), 'rb') as pickle_file:
        permanent_riders = pd.DataFrame(pickle.load(pickle_file))
    
    with open(os.path.join(DATA_PATH, WEEKLY_SHEET_KEY), 'rb') as pickle_file:
        weekly_riders = pd.DataFrame(pickle.load(pickle_file))
    
    with open(os.path.join(DATA_PATH, DRIVER_SHEET_KEY), 'rb') as pickle_file:
        drivers = pd.DataFrame(pickle.load(pickle_file))
    
    prep.standardize_permanent_responses(permanent_riders)
    prep.standardize_weekly_responses(weekly_riders)
    
    # Reorder and rename columns before merging
    weekly_riders = weekly_riders[[WEEKLY_RIDER_TIMESTAMP_HDR, WEEKLY_RIDER_NAME_HDR, WEEKLY_RIDER_PHONE_HDR, WEEKLY_RIDER_LOCATION_HDR, WEEKLY_RIDER_FRIDAY_HDR, WEEKLY_RIDER_SUNDAY_HDR, WEEKLY_RIDER_NOTES_HDR]]
    weekly_riders.rename(columns={WEEKLY_RIDER_TIMESTAMP_HDR: RIDER_TIMESTAMP_HDR, WEEKLY_RIDER_NAME_HDR: RIDER_NAME_HDR, WEEKLY_RIDER_PHONE_HDR: RIDER_PHONE_HDR, WEEKLY_RIDER_LOCATION_HDR: RIDER_LOCATION_HDR, WEEKLY_RIDER_FRIDAY_HDR: RIDER_FRIDAY_HDR, WEEKLY_RIDER_SUNDAY_HDR: RIDER_SUNDAY_HDR, WEEKLY_RIDER_NOTES_HDR: RIDER_NOTES_HDR}, inplace=True)
    permanent_riders.rename(columns={PERMANENT_RIDER_TIMESTAMP_HDR: RIDER_TIMESTAMP_HDR, PERMANENT_RIDER_NAME_HDR: RIDER_NAME_HDR, PERMANENT_RIDER_PHONE_HDR: RIDER_PHONE_HDR, PERMANENT_RIDER_LOCATION_HDR: RIDER_LOCATION_HDR, PERMANENT_RIDER_FRIDAY_HDR: RIDER_FRIDAY_HDR, PERMANENT_RIDER_SUNDAY_HDR: RIDER_SUNDAY_HDR, PERMANENT_RIDER_NOTES_HDR: RIDER_NOTES_HDR}, inplace=True)
    riders = pd.concat([permanent_riders, weekly_riders])
    riders.reset_index(inplace=True, drop=True)

    return (drivers, riders)


def write_assignments(assignments: pd.DataFrame, update: bool):
    """Write the given dataframe to the output file. If update is True, write to final Google Sheet.
    """
    logging.info('Writing assignments')
    # write to pickle
    assignments.to_pickle(os.path.join(DATA_PATH, OUTPUT_SHEET_KEY))

    if update:
        with open(SHEET_IDS_FILE) as gid_json:
            gid_data = json.load(gid_json)

        # connect Google Sheets
        gc = gspread.service_account(filename=SERVICE_ACCT_FILE)
        ws = gc.open_by_key(gid_data[OUTPUT_SHEET_KEY]).get_worksheet(0)

        ws.resize(rows=len(assignments))
        ws.update([assignments.columns.values.tolist()] + assignments.values.tolist())
        logging.info('Uploading assignments')


def get_cached_output() -> pd.DataFrame:
    """Get the assignments that were calculated from the last grouping.
    """
    with open(os.path.join(DATA_PATH, OUTPUT_SHEET_KEY), 'rb') as out:
        return pd.DataFrame(pickle.load(out))


def update_drivers_locally(drivers_df: pd.DataFrame):
    """Write the given dataframe to the drivers pickle file.
    """
    drivers_df.to_pickle(os.path.join(DATA_PATH, DRIVER_SHEET_KEY))