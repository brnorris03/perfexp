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

battery_state = "/proc/acpi/battery/BAT0/state"

#$ cat /proc/acpi/battery/BAT0/state 
#present:                 yes
#capacity state:          ok
#charging state:          charging
#present rate:            577 mA
#remaining capacity:      4627 mAh
#present voltage:         12587 mV
#
# or
#
#present:                 yes
#capacity state:          ok
#charging state:          discharging
#present rate:            16386 mW
#remaining capacity:      44330 mWh
#present voltage:         12120 mV


re_rate     = re.compile('^present rate:\s+([0-9]+)')
re_capacity = re.compile('^remaining capacity:\s+(0-9]+)')
re_voltage  = re.compile('^present voltage:\s+([0-9]+)')


def get_watt():
    rate = 0.0
    capacity = 0.0
    voltage = 0.0

    f = open( battery_state )
    while True:
        line = f.readline()
        if not line:
            break
        m = re_rate.match(line)
        if m:
            rate = int(m.group(1))

        m = re_capacity.match(line)
        if m:
            capacity = int(m.group(1))
            
        m = re_voltage.match(line)
        if m:
            voltage = int(m.group(1))

    #return float(rate * voltage)/1000.0/1000.0
    return float(rate)/1000.0

orig_time = time.time()
prev_time = time.time()
while (time.time() - orig_time) < duration :
    tmp = time.time()
    print '%lf %lf' % (tmp, get_watt())
#    while (time.time() - prev_time) < interval:
#        time.sleep(0.001)
#    prev_time = tmp
    time.sleep(interval)

sys.exit(0)






