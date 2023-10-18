""" Main file for automatic driver assignments.

Usage:
    usage: python rides.py [-h] --day {friday,sunday} [--fetch | --no-fetch] [--update | --no-update] [--rotate] [--threshold {1,2,3,4,5,6,7,8,9,10}] [--debug]
"""

from cfg.config import GLOBALS, GROUPING_THRESHOLD, SERVICE_ACCT_FILE
import lib
import os
import argparse


def main() -> None:
    """ Assign riders to drivers, updating the sheet if specified
    """
    # Fetch data from sheets
    if args['fetch']:
        lib.update_pickles()

    # Print input
    if args['debug']:
        lib.print_pickles()
    
    (drivers, riders) = lib.get_cached_input()
    lib.clean_data(drivers, riders)

    # Do requested preprocessing
    if args['rotate']:
        prev_out = lib.get_cached_output()
        # Rotate drivers by last date driven
        lib.rotate_drivers(drivers, lib.get_prev_driver_phones(prev_out))
        lib.update_drivers_locally(drivers)

    # Execute the assignment algorithm
    if args['day'] == 'friday':
        out = lib.assign_friday(drivers, riders, args['debug'])
    else:
        out = lib.assign_sunday(drivers, riders, args['debug'])
    
    # Print output
    if args['debug']:
        print('Assignments output')
        print(out)

    lib.write_assignments(out, args['update'])


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--day', required=True, choices=['friday', 'sunday'],
                        help='choose either \'friday\' for CL, or \'sunday\' for church')
    parser.add_argument('--fetch', action=argparse.BooleanOptionalAction, default=True,
                        help='choose whether to download Google Sheets data')
    parser.add_argument('--update', action=argparse.BooleanOptionalAction, default=True,
                        help='choose whether to upload output to Google Sheets')
    parser.add_argument('--rotate', action='store_true',
                        help='previous assignments are cleared and drivers are rotated based on date last driven')
    parser.add_argument('--threshold', type=int, default=2, choices=range(1, 11),
                        help='sets how many open spots a driver must have to spontaneously pick up at a neighboring location')
    parser.add_argument('--debug', action='store_true',
                        help='prints out debug statements while running')
    
    args = vars(parser.parse_args())

    GLOBALS[GROUPING_THRESHOLD] = args['threshold']

    api_reqs_fulfilled = os.path.exists(SERVICE_ACCT_FILE) or not (args['update'] or args['fetch']) 
    execute = api_reqs_fulfilled

    if api_reqs_fulfilled:
        main()
    else:
        print(f'${SERVICE_ACCT_FILE} not found.')
        print('Make sure service_account.json is in the cfg directory.')
        print("Contact Timothy Wu if you don't have it.")
