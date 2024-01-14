"""Implements all the postprocessing functionality for the results.
"""

from cfg.config import *
import logging
import numpy as np
import pandas as pd


def clean_output(out: pd.DataFrame):
    """Filters out the unneeded columns and and validates the data before writing.
    """
    _format_output(out)


def _format_output(out: pd.DataFrame):
    """Organizes the output to order by driver then driver. Removes redundant driver details.
    """
    out.sort_values(by=[OUTPUT_DRIVER_NAME_HDR, RIDER_LOCATION_HDR], inplace=True)
    out.reset_index(inplace=True, drop=True)

    for idx in range(len(out) - 1, -1, -1):
        if out.at[idx, OUTPUT_DRIVER_NAME_HDR] is np.nan:
            # Denote unassigned riders.
            out.at[idx, OUTPUT_DRIVER_NAME_HDR] = '?'
            out.at[idx, OUTPUT_DRIVER_PHONE_HDR] = '?'
            out.at[idx, OUTPUT_DRIVER_CAPACITY_HDR] = ''
            logging.debug(f'_format_output --- \t{out.at[idx, RIDER_NAME_HDR]} has no driver')
        elif idx > 0 and out.at[idx, OUTPUT_DRIVER_NAME_HDR] == out.at[idx - 1, OUTPUT_DRIVER_NAME_HDR]:
            # Remove redundant driver details.
            out.at[idx, OUTPUT_DRIVER_NAME_HDR] = ''
            out.at[idx, OUTPUT_DRIVER_PHONE_HDR] = ''
            out.at[idx, OUTPUT_DRIVER_CAPACITY_HDR] = ''