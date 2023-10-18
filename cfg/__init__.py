from cfg.config import *

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
                if place not in loc_map:
                    loc_map[place] = LOC_NONE
                loc_map[place] |= loc
            loc <<= 1
except:
    print(f'${MAP_FILE} not loaded. Location optimizations are ignored.')

"""Loads ignore_drivers.txt into a list.
"""
try:
    with open(IGNORE_DRIVERS_FILE, 'r') as nums:
        for num in nums:
            ignored_drivers.append(num.strip())
except:
    print(f'${IGNORE_DRIVERS_FILE} not loaded. No drivers ignored.')

"""Loads ignore_riders.txt into a list.
"""
try:
    with open(IGNORE_RIDERS_FILE, 'r') as nums:
        for num in nums:
            ignored_riders.append(num.strip())
except:
    print(f'${IGNORE_RIDERS_FILE} not loaded. No riders ignored.')

"""Create cache files.
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