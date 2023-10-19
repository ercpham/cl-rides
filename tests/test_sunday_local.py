"""Test script for sunday, no fetching or updating.
"""

import os
import sys
curr = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(curr))

import rides

args = {
    'day': 'sunday',
    'fetch': False,
    'update': False,
    'rotate': False,
    'threshold': 2,
    'log': 'INFO'
}

rides.main(args)