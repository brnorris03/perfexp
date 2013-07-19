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
    #arch.get_tlb(reps='3')
    #arch.get_create_delete_perf()
    #arch.get_cacheline_lmbench()
    #arch.get_pipe_latency()
    #arch.get_pipe_bw()
    arch.get_ior_avail_caller(reps='2', options='-F')
    #arch.get_papi_avail_caller()
    #arch.get_perfsuite_avail_caller()
    #arch.get_blackjack_avail_caller()
    #arch.get_basic_proc_ops()
    #arch.get_pipe_latency()
    #arch.get_network_latency(procs='1', reps='2', server='',comm='localhost', lat_type='tcp')
    #arch.get_context_switches(procs='2',size='100',reps='2',contexts='3 4 5 7 12')
    #arch.get_syscall_ovrhds(procs='2', reps='2', test_open='tests.py')
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
