#!/usr/bin/env python

#
# HEATER.FPUARCH(MFlops): AGG= 55712.40  MEAN=  464.27  MIN=  463.43  MAX=  464.64  SD=    0.21
# HEATER.FPU    (MFlops): AGG=102265.77  MEAN=  852.21  MIN=  842.22  MAX=  856.77  SD=    5.24
# HEATER.MEMCPY (  MB/s): AGG= 47347.43  MEAN=  394.56  MIN=  273.90  MAX=  546.16  SD=  100.01
# HEATER.MEMCPY (  MB/s): AGG=353107.23  MEAN= 2942.56  MIN= 2937.94  MAX= 2945.76  SD=    1.38
# HEATER.MEMCPY (  MB/s): AGG=237308.42  MEAN= 1977.57  MIN=  515.72  MAX= 4140.06  SD=  861.41
# HEATER.RANDOM (  MB/s): AGG=  3475.25  MEAN=   28.96  MIN=   26.97  MAX=   30.80  SD=    1.20
# HEATER.RANDOM (  MB/s): AGG= 73119.90  MEAN=  609.33  MIN=  607.45  MAX=  610.66  SD=    0.72
# HEATER.RANDOM (  MB/s): AGG= 25705.64  MEAN=  214.21  MIN=   58.14  MAX=  304.68  SD=   72.32
#
#36.1802790893249 148

import sys, re

start_time = 20.0
stop_time = 60.0

total_watt = 0.0
real_start_time = 0.0
real_stop_time = 0.0

re_head = re.compile( '^# HEATER\.(\w+)\s*\((.*)\).*MEAN=\s*([0-9.]+)' )

re_sample = re.compile( '([0-9.]+)\s+([0-9.]+)')

name=''
unit=''
value=0.0


prev_t = 0.0
prev_w = 0.0

while True:
    l=sys.stdin.readline()
    if not l:
        break
    m = re_sample.match(l)
    if m:
        t = float( m.group(1) )
        w = float( m.group(2) )
        if real_start_time == 0.0 and t >= start_time :
            real_start_time = t
            prev_t = t
            prev_w = w
        elif t >= stop_time :
            break
        elif real_start_time > 0.0 :
            real_stop_time = t

            # approximation. assume that the power is constant between
            # the previous sampling point and the current sampling
            # point.
            
            total_watt = total_watt + prev_w*(t-prev_t)
            prev_w = w
            prev_t = t

    m = re_head.match(l)
    if m:
        name  = m.group(1)
        unit  = m.group(2)
        value = float( m.group(3) )


#print real_start_time, real_stop_time, total_watt

a = total_watt / ( real_stop_time-real_start_time)

#print '%-10s: %lf %s' % (name, value, unit)
#print '%-10s: %lf %s' % ('power',a, 'watt')

print '%-10s:  %10.3lf %s/watt' % (name, (value/a),unit)





