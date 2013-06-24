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

        # The number of time to run the experiment for each measurement
        #self.reps = 5
        pass


    def runBenchmark(self, cmd):
        # TODO: run entire benchmark 
        return

    def get_mem_read_bw(self, **kwargs): 
        ''' Memory read bandwidth measurement with lmbench '''
        size = kwargs.get('size')
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        cmd = self.lmbench_path + 'bw_mem -P %s %s rd' % (procs,size)

        vals = []
        self.log(cmd)
        for i in range(0,int(reps)):
            # TODO KC: make the number of repetitions a parameter
            """made it one of the inputs in the test file and added it to
            params. Commented out the repetitions in self. Was it supposed
            to be an input parameter or stay as a class varialbe?"""
            return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
            s,val = cmd_output.split()
            vals.append(float(val))
             
        params = {'metric':'mem_read_bw','size':s,'procs':procs,'reps':reps}
        self.recordMeasurement(params, Measurement(get_stats(vals),units='MB/s',params=params))
        return

    def get_l1_read_latency(self, **kwargs):
        ''' Measure L1 read latency and record in self.measurements. '''
        # TODO KC
        size = kwargs.get('size')
        stride = kwargs.get('stride')
        cmd = self.lmbench_path + 'lat_mem_rd %s %s' % (size, stride)
        self.log(cmd)
        #get output
        return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
        
        #find only numbers without alpha characters
        p = re.compile('\d+')
        val = p.findall(cmd_output)
        mes = { }
        if (len(val)%2 == 0):
            #pair them up
            for i in range(0, len(val), 2):
                mes[val[i]] =val[i+1] 
        else:
            print "error: not a match"

        params = {'metric':'l1_read_latency', 'size':size, 'stride':stride}
        self.recordMeasurement(params, mes)

        return

    def get_l1_read_bw(self, **kwargs):
        ''' Measure L1 read bandwidth and record in self.measurements. '''
        # TODO KC
        size = kwargs.get('size')
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        cmd = self.lmbench_path + 'bw_mem -P %s %s rd' % (procs,size)

        vals = []
        self.log(cmd)
        for i in range(0,int(reps)):
            return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
            s,val = cmd_output.split()
            vals.append(float(val))
             
        params = {'metric':'l1_read_bw','size':s,'procs':procs,'reps':reps}
        self.recordMeasurement(params, Measurement(get_stats(vals),units='MB/s',params=params))

        return



    def log(self, thestr):
        f = open(self.logfile,"a")
        f.write("%s\n" % thestr)
        f.close()

    def recordMeasurement(self, params, measurement):
        ''' Record the measurement and relevant parameters in the log file. '''
        key = str(params)
        self.measurements[key] = measurement
        f = open(self.logfile,"a")
        f.write("%s\n" % str(self.measurements[key]))
        f.close()

