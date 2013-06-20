#!/usr/bin/env python

import os, sys, getopt

from bench.interfaces import AbstractPlatform, Measurement
from common.messages import err,warn,info,debug,exit
from common.utils import system_or_die, get_stats

class X86(AbstractPlatform):
    def __init__(self):
        AbstractPlatform.__init__(self)
        # temporarily hard-coded location of lmbench (on cookie):
        self.lmbench_path = '/disks/soft/src/lmbench3/bin/x86_64-linux-gnu/'
        # LMBench: http://www.bitmover.com/lmbench

        self.logfile = os.path.join(os.getcwd(),'X86.log')
        pass


    def runBenchmark(self, cmd):
        # TODO: run entire benchmark 
        return

    def get_mem_read_bw(self, **kwargs): 
        ''' Memory read bandwidth measurement with lmbench '''
        size = kwargs.get('size')
        procs = kwargs.get('procs')
        cmd = self.lmbench_path + 'bw_mem -P %s %s rd' % (procs,size)

        vals = []
        self.log(cmd)
        for i in range(1,20):
            # TODO KC: make the number of repetitions a parameter
            return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
            s,val = cmd_output.split()
            vals.append(float(val))
             
        params = ['mem_read_latency',s]
        self.recordMeasurement('mem_read_latency', Measurement(get_stats(vals),units='MB/s',params=params))
        return

    def get_l1_read_latency(self, **kwargs):
        ''' Measure L1 read latency and record in self.measurements. '''
        # TODO KC
        return

    def get_l1_read_bw(self, **kwargs):
        ''' Measure L1 read bandwidth and record in self.measurements. '''
        # TODO KC
        return



    def log(self, thestr):
        f = open(self.logfile,"a")
        f.write("%s\n" % thestr)
        f.close()

    def recordMeasurement(self, metric, measurement):
        self.measurements[metric] = measurement
        f = open(self.logfile,"a")
        f.write("%s : %s\n" % (metric,str(self.measurements[metric])))
        f.close()

# --------------------------------------------------
# --- code for testing of this class only ----------


def process(arg):
    pass

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            x86().help()
            print __doc__
            sys.exit(0)

    # process arguments
    for arg in args:
        process(arg) # process() is defined elsewhere

if __name__ == "__main__":
    main()
