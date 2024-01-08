""" Main file for automatic driver assignments.
"""

import cfg
from cfg.config import *
import lib.assignments as core
import lib.preprocessing as prep
import lib.rides_data as data
import os
import argparse
import logging


def main(args: dict) -> None:
    """ Assign riders to drivers, updating the sheet if specified
    """

    logging.basicConfig(format='%(levelname)s:%(message)s', level=getattr(logging, args['log'].upper()))

    # Continue only if service_account.json exists for accessing the Google Sheets data
    api_reqs_fulfilled = os.path.exists(SERVICE_ACCT_FILE) or not (args['download'] or args['upload']) 
    if not api_reqs_fulfilled:
        logging.critical(f'${SERVICE_ACCT_FILE} not found.')
        logging.critical('Make sure service_account.json is in the cfg directory.')
        logging.critical("Contact Timothy Wu if you don't have it.")
        return

    cfg.load(args)

    # Fetch data from sheets
    if args['download']:
        data.update_pickles()

    # Print input
    data.print_pickles()
    
    (drivers, riders) = data.get_cached_input()

    if len(riders.index) == 0:
        logging.error('No riders, aborting')
        return
    if len(drivers.index) == 0:
        logging.error('No drivers, aborting')
        return

    if ARGS['rotate']:
        prep.rotate_drivers(drivers)

    prep.clean_data(drivers, riders)
    
    # Execute the assignment algorithm
    if args['day'] == 'friday':
        out = core.assign_friday(drivers, riders)
    else:
        out = core.assign_sunday(drivers, riders)
    
    # Print output
    logging.debug(f'Assignments output\n{out}')

    data.write_assignments(out, args['upload'])


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--day', required=True, choices=['friday', 'sunday'],
                        help='choose either \'friday\' for CL, or \'sunday\' for church')
    parser.add_argument('--main-service', default=SECOND_SERVICE, choices=[FIRST_SERVICE, SECOND_SERVICE],
                        help='select the main Sunday service (i.e. select 1st service during weeks with ACE classes)')
    parser.add_argument('--rotate', action='store_true',
                        help='drivers are rotated based on date last driven')
    parser.add_argument('--just-weekly', action='store_true',
                        help='use only the weekly rides for for these assignments (i.e. holidays)')
    parser.add_argument('--download', action=argparse.BooleanOptionalAction, default=True,
                        help='choose whether to download Google Sheets data')
    parser.add_argument('--upload', action=argparse.BooleanOptionalAction, default=True,
                        help='choose whether to upload output to Google Sheets')
    parser.add_argument('--distance', type=int, default=2, choices=range(1, DISTANCE_MAX),
                        help='set how many far a driver can be to pick up at a neighboring location before choosing a last resort driver')
    parser.add_argument('--vacancy', type=int, default=2, choices=range(1, VACANCY_MAX),
                        help='set how many open spots a driver must have to pick up at a neighboring location before choosing a last resort driver')
    parser.add_argument('--log', default='INFO', choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help='set a level of verbosity for logging')
    
    args = vars(parser.parse_args())

    main(args);
