# This file is part of Contractor
# Original author: James Amundson, amundson@fnal.gov
# (c) 2007-2010 Fermi Research Alliance, LLC
# (c) 2011 Tech-X Corporation
# For copying information, see the file LICENSE

#!/usr/bin/env python

import time
from messages import info

_start_time = 0.0

def reset_timer():
    global _start_time
    _start_time = time.time()

def show_timer():
    global _start_time
    info("total time:",end=' ')
    seconds = time.time() - _start_time
    hours = int(seconds/3600)
    if hours > 0:
        info(str(hours) + " hours,", end=' ')
        seconds = seconds - 3600*hours
    minutes = int(seconds/60)
    if minutes > 0:
        info(str(minutes) + " minutes,", end=' ')
        seconds = seconds - 60*minutes
    info("%0.3g seconds" % seconds)
