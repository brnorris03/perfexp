#!/usr/bin/env python

import os
import sys
import re
import time

if len(sys.argv) < 4 :
    print "Usage: micwatt.py card_no duration(sec) interval(sec)"
    sys.exit(1)

cardno = int(sys.argv[1])
duration = int(sys.argv[2])
interval = int(sys.argv[3])

#Card 1 (freq):
#   Core Frequency: .......... 1.05 GHz
#   Total Power: ............. 130 Watts

re_card_no = re.compile('Card\s+([0-9])')
re_watt    = re.compile('\s+Total Power:[ .]+([0-9]+)')
re_freq    = re.compile('\s+Core Frequency:[ .]+([0-9.]+)')

def get_watt():
    currentcardno = 0
    watt = 0
    freq = 0

    f = os.popen( "micsmc -f 2>/dev/null", "r" )  # XXX: may hide important error
    line = f.readline()
    while line:
        m = re_card_no.match(line)
        if m:
            currentcardno = int(m.group(1))

        m = re_freq.match(line)
        if m:
            freq = float(m.group(1))

        m = re_watt.match(line)
        if m:
            watt = int(m.group(1))
            if cardno == currentcardno :
                break
        line = f.readline()
    return watt, freq

orig_time = time.time()
while (time.time() - orig_time) < duration :
    tmp = time.time()
    w, f = get_watt()
    print '%lf %d # freq=%lf' % (tmp, w, f)
    sys.stdout.flush()
    while (time.time() - tmp) < interval:
        time.sleep(0.01)

sys.exit(0)
