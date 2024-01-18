"""Implements all the postprocessing functionality for the results.
"""

from cfg.config import *
import logging
import numpy as np
import pandas as pd


def clean_output(out: pd.DataFrame) -> pd.DataFrame:
    """Filters out the unneeded columns and and validates the data before writing.
    """
    return _format_output(out)


def _format_output(out: pd.DataFrame) -> pd.DataFrame:
    """Organizes the output to order by driver then driver. Removes redundant driver details.
    """
    out.sort_values(by=[OUTPUT_DRIVER_NAME_HDR, RIDER_LOCATION_HDR], inplace=True)
    out.reset_index(inplace=True, drop=True)

    driver_cnt = 1
    for idx in range(len(out) - 1):
        if out.at[idx, OUTPUT_DRIVER_NAME_HDR] != out.at[idx + 1, OUTPUT_DRIVER_NAME_HDR]:
            driver_cnt += 1
 
    # Append enough rows to space out drivers
    total_rows = driver_cnt + len(out)
    offset = driver_cnt
    new_out = pd.DataFrame({OUTPUT_DRIVER_NAME_HDR: [''] * total_rows,
                            OUTPUT_DRIVER_PHONE_HDR: [''] * total_rows,
                            OUTPUT_DRIVER_CAPACITY_HDR: [''] * total_rows,
                            RIDER_NAME_HDR: [''] * total_rows,
                            RIDER_PHONE_HDR: [''] * total_rows,
                            RIDER_LOCATION_HDR: [''] * total_rows,
                            RIDER_NOTES_HDR: [''] * total_rows
                            })
        
    offset = driver_cnt
    for idx in range(len(out) - 1, -1, -1):
        skip = False
        if out.at[idx, OUTPUT_DRIVER_NAME_HDR] is np.nan:

            if idx == 0 or out.at[idx, OUTPUT_DRIVER_NAME_HDR] != out.at[idx - 1, OUTPUT_DRIVER_NAME_HDR]:
                skip = True
            # Denote unassigned riders.
            out.at[idx, OUTPUT_DRIVER_NAME_HDR] = '?'
            out.at[idx, OUTPUT_DRIVER_PHONE_HDR] = '?'
            out.at[idx, OUTPUT_DRIVER_CAPACITY_HDR] = ''
            logging.debug(f'_format_output --- {out.at[idx, RIDER_NAME_HDR]} has no driver')
            
        elif idx > 0 and out.at[idx, OUTPUT_DRIVER_NAME_HDR] == out.at[idx - 1, OUTPUT_DRIVER_NAME_HDR]:
            # Remove redundant driver details.
            out.at[idx, OUTPUT_DRIVER_NAME_HDR] = ''
            out.at[idx, OUTPUT_DRIVER_PHONE_HDR] = ''
            out.at[idx, OUTPUT_DRIVER_CAPACITY_HDR] = ''
        else:
            skip = True

        _copy_output_row(out, new_out, idx, idx + offset)
        if skip:
            offset -= 1
    
    return new_out

        
def _copy_output_row(src: pd.DataFrame, dst: pd.DataFrame, src_idx: int, dst_idx: int):
    dst.at[dst_idx, OUTPUT_DRIVER_NAME_HDR] = src.at[src_idx, OUTPUT_DRIVER_NAME_HDR]
    dst.at[dst_idx, OUTPUT_DRIVER_PHONE_HDR] = src.at[src_idx, OUTPUT_DRIVER_PHONE_HDR]
    dst.at[dst_idx, OUTPUT_DRIVER_CAPACITY_HDR] = src.at[src_idx, OUTPUT_DRIVER_CAPACITY_HDR]
    dst.at[dst_idx, RIDER_NAME_HDR] = src.at[src_idx, RIDER_NAME_HDR]
    dst.at[dst_idx, RIDER_PHONE_HDR] = src.at[src_idx, RIDER_PHONE_HDR]
    dst.at[dst_idx, RIDER_LOCATION_HDR] = src.at[src_idx, RIDER_LOCATION_HDR]
    dst.at[dst_idx, RIDER_NOTES_HDR] = src.at[src_idx, RIDER_NOTES_HDR]