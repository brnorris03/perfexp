#!/usr/bin/env python

import sys, getopt

from bench.platforms import x86

def main():
    # Add any tests in here or separte functions, this is for development/debugging only
    arch = x86.X86()   #makes arch an instance of the X86 class?
    
    # print list of metrics (this is defined in bench/interfaces.py)
    arch.help()

    # test various metrics computations

    #arch.measure('mem_read_bw', procs='1', size='256m', reps='5')
    #arch.measure('mem_read_bw', procs='2', size='256m', reps='1')
    #arch.measure('l1_read_latency', size='32', stride='128', level='2')
    arch.measure('l1_read_bw', procs='1', size='258', next_size = '265', reps='1')


    # Print all measurements
    for key,val in arch.measurements.items():
        print val




if __name__ == "__main__":
    main()
