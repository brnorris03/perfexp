#!/usr/bin/env python

import sys, getopt

from bench.platforms import x86

def main():
    # Add any tests in here or separte functions, this is for development/debugging only
    arch = x86.X86()
    
    # print list of metrics (this is defined in bench/interfaces.py)
    arch.help()

    # test various metrics computations

    arch.measure('mem_read_bw', procs='1', size='256m')
    #arch.measure('mem_read_latency')


    # Print all measurements
    print arch.measurements




if __name__ == "__main__":
    main()
