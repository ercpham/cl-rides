"""Test script for sunday, no fetching or updating.
"""

import os
import sys
curr = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(curr))

import rides

rides.main(False, False, False, False, False, True)