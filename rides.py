""" Main file for automatic driver assignments.

Usage:
    usage: rides.py [-h] --day {friday,sunday} [--fetch | --no-fetch] [--update | --no-update] [--rotate]
                [--threshold {1,2,3,4,5,6,7,8,9,10}] [--log {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
"""

import cfg
from cfg.config import GLOBALS, DISTANCE_THRESHOLD, DISTANCE_MAX, VACANCY_THRESHOLD, VACANCY_MAX, SERVICE_ACCT_FILE
import lib
import os
import argparse
import logging


def main(args: dict) -> None:
    """ Assign riders to drivers, updating the sheet if specified
    """

    cfg.load()

    # Fetch data from sheets
    if args['download']:
        lib.update_pickles()

    # Print input
    lib.print_pickles()
    
    (drivers, riders) = lib.get_cached_input()
    lib.clean_data(drivers, riders)

    # Do requested preprocessing
    if args['rotate']:
        prev_out = lib.get_cached_output()
        # Rotate drivers by last date driven
        lib.rotate_drivers(drivers, lib.get_prev_driver_phones(prev_out))
        lib.update_drivers_locally(drivers)
        logging.debug(f'Rotating drivers\n{drivers}')

    # Execute the assignment algorithm
    if args['day'] == 'friday':
        out = lib.assign_friday(drivers, riders)
    else:
        out = lib.assign_sunday(drivers, riders)
    
    # Print output
    logging.debug(f'Assignments output\n{out}')

    lib.write_assignments(out, args['upload'])


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--day', required=True, choices=['friday', 'sunday'],
                        help='choose either \'friday\' for CL, or \'sunday\' for church')
    parser.add_argument('--download', action=argparse.BooleanOptionalAction, default=True,
                        help='choose whether to download Google Sheets data')
    parser.add_argument('--upload', action=argparse.BooleanOptionalAction, default=True,
                        help='choose whether to upload output to Google Sheets')
    parser.add_argument('--rotate', action='store_true',
                        help='previous assignments are cleared and drivers are rotated based on date last driven')
    parser.add_argument('--distance', type=int, default=2, choices=range(1, DISTANCE_MAX),
                        help='set how many far a driver can be to pick up at a neighboring location before choosing a last resort driver')
    parser.add_argument('--vacancy', type=int, default=2, choices=range(1, VACANCY_MAX),
                        help='set how many open spots a driver must have to pick up at a neighboring location before choosing a last resort driver')
    parser.add_argument('--log', default='INFO', choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help='set a level of verbosity for logging')
    
    args = vars(parser.parse_args())

    logging.basicConfig(format='%(levelname)s:%(message)s', level=getattr(logging, args['log'].upper()))

    GLOBALS[DISTANCE_THRESHOLD] = args['distance']
    GLOBALS[VACANCY_THRESHOLD] = args['vacancy']

    api_reqs_fulfilled = os.path.exists(SERVICE_ACCT_FILE) or not (args['download'] or args['upload']) 

    if api_reqs_fulfilled:
        main(args)
    else:
        logging.critical(f'${SERVICE_ACCT_FILE} not found.')
        logging.critical('Make sure service_account.json is in the cfg directory.')
        logging.critical("Contact Timothy Wu if you don't have it.")
