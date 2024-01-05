from cfg.config import *
import logging
import os


def load_map(day: str):
    """Loads map.txt into a dictionary of bitmaps for the hardcoded locations.
    """
    specific_map = f'{os.path.dirname(MAP_FILE)}/{day}_{os.path.basename(MAP_FILE)}'
    if os.path.isfile(specific_map):
        map_file = specific_map
    elif os.path.isfile(MAP_FILE):
        map_file = MAP_FILE
    else:
        logging.info(f'{os.path.basename(specific_map)} and {os.path.basename(MAP_FILE)} not found. Location optimizations are ignored.')
        return

    cnt = 0
    with open(map_file, 'r') as map:
        loc = 0b1
        for line in map:
            if (line.startswith('#')):
                continue
            places = line.split(',')
            places = [place.strip() for place in places]
            for place in places:
                if place not in LOC_MAP:
                    LOC_MAP[place] = LOC_NONE
                LOC_MAP[place] |= loc
            loc <<= 1
            cnt += 1

    logging.info(f'{os.path.basename(map_file)} loaded with size={cnt}.')


def load_ignored_drivers():
    """Loads the list of drivers to skip.
    """
    try:
        cnt = 0
        with open(IGNORE_DRIVERS_FILE, 'r') as nums:
            for num in nums:
                IGNORED_DRIVERS.append(num.strip())
                cnt += 1
        logging.info(f'Ignoring {cnt} drivers.')
    except:
        logging.info(f'{os.path.basename(IGNORE_DRIVERS_FILE)} not found. No drivers ignored.')


def load_ignored_riders():
    """Loads the list of riders to skip.
    """
    try:
        cnt = 0
        with open(IGNORE_RIDERS_FILE, 'r') as nums:
            for num in nums:
                IGNORED_RIDERS.append(num.strip())
                cnt += 1
        logging.info(f'Ignoring {cnt} riders.')
    except:
        logging.info(f'{os.path.basename(IGNORE_RIDERS_FILE)} not found. No riders ignored.')


def load_driver_prefs():
    """Loads the preferred locations of drivers.
    """
    try:
        cnt = 0
        with open(DRIVER_PREFS_FILE, 'r') as prefs:
            for pref in prefs:
                pref = pref.split(',')
                phone = pref[1].strip()
                loc = pref[2].strip()
                DRIVER_PREFS[phone] = LOC_MAP.get(loc, LOC_NONE)
                cnt += 1
        logging.info(f'Loaded {cnt} driver preferences.')
    except:
        logging.info(f'{os.path.basename(DRIVER_PREFS_FILE)} not found. No driver preferences.')


def create_pickles():
    """Create cache files in pickle directory.
    """
    if (not os.path.isdir(DATA_PATH)):
        os.makedirs(DATA_PATH)
    import pandas as pd
    if (not os.path.exists(os.path.join(DATA_PATH, PERMANENT_SHEET_KEY))):
        pd.DataFrame().to_pickle(os.path.join(DATA_PATH, PERMANENT_SHEET_KEY))
    if (not os.path.exists(os.path.join(DATA_PATH, WEEKLY_SHEET_KEY))):
        pd.DataFrame().to_pickle(os.path.join(DATA_PATH, WEEKLY_SHEET_KEY))
    if (not os.path.exists(os.path.join(DATA_PATH, DRIVER_SHEET_KEY))):
        pd.DataFrame().to_pickle(os.path.join(DATA_PATH, DRIVER_SHEET_KEY))
    if (not os.path.exists(os.path.join(DATA_PATH, OUTPUT_SHEET_KEY))):
        pd.DataFrame().to_pickle(os.path.join(DATA_PATH, OUTPUT_SHEET_KEY))


def load(day: str):
    load_map(day)
    load_ignored_drivers()
    load_ignored_riders()
    load_driver_prefs()
    create_pickles()