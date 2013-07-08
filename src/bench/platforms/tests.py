#!/usr/bin/env python

import os, sys, getopt

abs_path = os.path.realpath(sys.argv[0])
cur_dir = os.path.dirname(abs_path)
mydir = os.path.join(cur_dir,'..','..')
print mydir
sys.path.extend([mydir])

from bench.platforms import x86

def main():
    
    # Add any tests in here or separate functions, this is for development/debugging only
    arch = x86.X86()   #makes arch an instance of the X86 class?
    
    # print list of metrics (this is defined in bench/interfaces.py)
    arch.help()

    # test various metrics computations
    #arch.get_hardware_specs()
    #arch.get_process_creation(procs='1', reps='5')
    arch.get_context_switches(procs='1',size='100',reps='2',contexts='3 4 5 7 12')
    arch.get_syscall_ovrhds(procs='1', reps='2', test_open='tests.py')
    #arch.measure('mem_write_bw', procs='1', size='256m', reps='5')
    #arch.measure('mem_read_bw', procs='1', size='256m', reps='5')
    #arch.measure('mem_read_bw', procs='2', size='256m', reps='1')
    #print arch.measure('l1_read_latency', procs='1', reps='1')
    #print arch.measure('l2_read_latency', procs='1', reps='1')
    #print arch.measure('mem_read_latency', procs='1', reps='1')

    #arch.measure('l1_read_bw', procs='1', size='258', next_size = '265', reps='1')

    # Print all measurements
    for key,val in arch.measurements.items():
        print val




if __name__ == "__main__":
    main()
