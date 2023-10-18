"""Implements all the postprocessing functionality for the results.
"""

from cfg.config import *
import numpy as np
import pandas as pd


def clean_output(out: pd.DataFrame):
    """Filters out the unneeded columns and and validates the data before writing.
    """
    _format_output(out)


def _format_output(out: pd.DataFrame):
    """Organizes the output to order by driver then driver. Removes redundant driver details.
    """
    out.sort_values(by=[OUTPUT_DRIVER_NAME_KEY, RIDER_LOCATION_KEY], inplace=True)
    out.reset_index(inplace=True, drop=True)

    for idx in range(len(out) - 1, -1, -1):
        if out.at[idx, OUTPUT_DRIVER_NAME_KEY] is np.nan:
            # Denote unassigned riders.
            out.at[idx, OUTPUT_DRIVER_NAME_KEY] = '?'
            out.at[idx, OUTPUT_DRIVER_PHONE_KEY] = '?'
            out.at[idx, OUTPUT_DRIVER_CAPACITY_KEY] = ''
        elif idx > 0 and out.at[idx, OUTPUT_DRIVER_NAME_KEY] == out.at[idx - 1, OUTPUT_DRIVER_NAME_KEY]:
            # Remove redundant driver details.
            out.at[idx, OUTPUT_DRIVER_NAME_KEY] = ''
            out.at[idx, OUTPUT_DRIVER_PHONE_KEY] = ''
            out.at[idx, OUTPUT_DRIVER_CAPACITY_KEY] = ''


def alert_skipped_riders(out: pd.DataFrame, debug: bool):
    """Prints out all the riders who do not have a driver."""
    if debug:
        print("Printing stranded riders.")
        for _, rider in out.iterrows():
            if rider[OUTPUT_DRIVER_NAME_KEY] is np.NaN:
                print(f'\t{rider[RIDER_NAME_KEY]} has no driver')
        print()