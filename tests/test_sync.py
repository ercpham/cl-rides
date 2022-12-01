"""Test script for synchonizing previous output to current output.
"""

import os
import sys
curr = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(curr))

import lib.preprocessing as prep
import lib.rides_data as data

prep.load_cfg()
(drivers, riders) = data.get_cached_input()
prev_out = data.get_cached_output()
prep.clean_data(drivers, riders)

print('Drivers ------------------------------------')
print(drivers)
print()
print('Riders -------------------------------------')
print(riders)
print()
print('Previous assignments -----------------------')
print(prev_out)
print()

riders = prep.filter_sunday(riders)
prep._add_temporaries(drivers)
out = prep.sync_to_last_assignments(drivers, riders, prev_out)

print('Drivers OUT --------------------------------')
print(drivers)
print()
print('Riders OUT ---------------------------------')
print(riders)
print()
print('Assignments OUT ----------------------------')
print(out)
print()