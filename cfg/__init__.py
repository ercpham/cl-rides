from cfg.config import *

def load_map():
    """Loads map.txt into a dictionary of bitmaps for the hardcoded locations.
    """
    try:
        with open(MAP_FILE, 'r') as map:
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
    except:
        print(f'${MAP_FILE} not loaded. Location optimizations are ignored.')

def load_ignored_drivers():
    """Loads the list of drivers to skip.
    """
    try:
        with open(IGNORE_DRIVERS_FILE, 'r') as nums:
            for num in nums:
                IGNORED_DRIVERS.append(num.strip())
    except:
        print(f'${IGNORE_DRIVERS_FILE} not loaded. No drivers ignored.')

def load_ignored_riders():
    """Loads the list of riders to skip.
    """
    try:
        with open(IGNORE_RIDERS_FILE, 'r') as nums:
            for num in nums:
                IGNORED_RIDERS.append(num.strip())
    except:
        print(f'${IGNORE_RIDERS_FILE} not loaded. No riders ignored.')

def load_driver_prefs():
    """Loads the preferred locations of drivers.
    """
    try:
        with open(DRIVER_PREFS_FILE, 'r') as prefs:
            for pref in prefs:
                (phone, loc) = pref.split(',')
                phone = phone.strip()
                loc = loc.strip()
                DRIVER_PREFS[phone] = LOC_MAP.get(loc, LOC_NONE)
    except:
        print(f'${DRIVER_PREFS_FILE} not loaded. No driver preferences.')

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

def load():
    load_map()
    load_ignored_drivers()
    load_ignored_riders()
    load_driver_prefs()
    create_pickles()