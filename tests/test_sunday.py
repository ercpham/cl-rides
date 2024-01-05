"""Test script for sunday.
"""

import os
import sys
curr = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(curr))

import rides

args = {
    'day': 'sunday',
    'fetch': True,
    'update': True,
    'rotate': False,
    'threshold': 2,
    'log': 'INFO',
    'main-service': 2
}

rides.main(args)