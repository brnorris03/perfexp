#!/usr/bin/env python

import os
import sys
import re
import time

if len(sys.argv) < 3 :
    print "Usage: laptopwatt.py  duration(sec) interval(sec)"
    sys.exit(1)

duration = int(sys.argv[1])
interval = int(sys.argv[2])

current_now="/sys/class/power_supply/BAT0/current_now"
voltage_now="/sys/class/power_supply/BAT0/voltage_now"

def get_watt():
    cur = 0.0
    vol = 0.0
    f = open( current_now )
    line = f.readline()
    cur = float(line)
    cur = cur / 1000.0 / 1000.0 
    f.close()
    f = open( voltage_now )
    line = f.readline()
    vol = float(line)
    vol = vol / 1000.0 / 1000.0 
    f.close()
#    print vol, cur

    return vol*cur


orig_time = time.time()
prev_time = time.time()
while (time.time() - orig_time) < duration :
    tmp = time.time()
    print '%lf %lf' % (tmp, get_watt())
    while (time.time() - tmp) < interval:
        time.sleep(0.01)


sys.exit(0)






