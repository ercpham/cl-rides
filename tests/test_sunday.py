"""Test script for sunday.
"""

import os
import sys
curr = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(curr))

import rides

rides.main(True, True, False, False, False, True)