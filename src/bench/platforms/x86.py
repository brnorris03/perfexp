#!/usr/bin/env python

import os, sys, getopt, re, math

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
            """number of repetitions added as a parameter"""
            return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
            s,val = cmd_output.split()
            vals.append(float(val))
             
        params = {'metric':'mem_read_bw','size':s,'procs':procs,'reps':reps}
        self.recordMeasurement(params, Measurement(get_stats(vals),units='MB/s',params=params))
        return

    def get_l1_read_latency(self, **kwargs):
        ''' Measure L1 read latency and record in self.measurements. '''
        size = kwargs.get('size')
        stride = kwargs.get('stride')
        cmd = self.lmbench_path + 'lat_mem_rd %s %s' % (size, stride)
        self.log(cmd)
        #get output
        return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
        
        #find only numbers without alpha characters
        regex = '[-+]?[0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?'
        val = re.findall(regex, cmd_output)
        mes = { }
        
        #pair them up
        for i in range(1, len(val), 2):
           if(i+1 < len(val)):
               mes[val[i]] =val[i+1] 
       

        params = {'metric':'l1_read_latency', 'size':size, 'stride':stride}
        self.recordMeasurement(params, mes)

        return

    def get_l1_read_bw(self, **kwargs):
        ''' Measure L1 read bandwidth and record in self.measurements. '''
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
      
        #depending on size (which one you're looking for) can start around that range
        start = int(kwargs.get('size'))
        end = int(kwargs.get('next_size'))

        means = []
        stat_collector = { }

        for x in range(start, end):
            vals = []
            cmd = self.lmbench_path + 'bw_mem -P %s %s rd' %  (procs, str(x)+'m')
            self.log(cmd)
            #get read bandwidth for a specific size
            for i in range(0,int(reps)):
                """number of repetitions added as a parameter"""
                return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
                s,val = cmd_output.split()
                vals.append(float(val))

            #keep statistics to pass
            stat_collector[x] = get_stats(vals)
            value_to_jump = stat_collector[x]
            means.append(value_to_jump[0])
            
        jumps = { }
        #get differences between values to find biggest jump
        for i in range(0, len(means)):
            if(i+1 < len(means)):
                jumps[means[i]] = float(abs(means[i+1] - means[i]))
                    
        #find the maximum jump
        maximum = 0
        track = -1
        for i in jumps:
            if(jumps[i] > maximum):
                maximum = jumps[i] 
                track = i
       
        mem_size = 0
        best = []
        #find final answers by looking through stat_collector
        for k, v in stat_collector.iteritems():
            if (v[0] == track):
                best = v
                mem_size = k

        #process vals 
        params = {'metric':'l1_read_bw','size':str(mem_size)+'m','procs':procs,'reps':reps}
        self.recordMeasurement(params, Measurement(best,units='MB/s',params=params))

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

