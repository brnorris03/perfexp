#!/usr/bin/env python

import os, sys, getopt, re, math

from bench.interfaces import AbstractPlatform, Measurement, MeasurementException
from common.messages import err,warn,info,debug,exit
from common.utils import system_or_die, get_stats

class X86(AbstractPlatform):
    def __init__(self):
        AbstractPlatform.__init__(self)
        # temporarily hard-coded location of lmbench (on cookie):
        self.lmbench_path = '/disks/soft/src/lmbench3/bin/x86_64-linux-gnu/'
        # LMBench: http://www.bitmover.com/lmbench
        self.papi_path = '/disks/soft/papi-4.4.0/bin/papi_avail'
        

        # TODO change 4 to the actual number of memory levels (incl. caches and main memory)
        self.memory_levels = 3
        
        # An array of Measurement objects for each level of the memory hierarchy
        # starting with L1
        self.datalatency = []  # data caches and main memory
        self.instrlatency = []  # instruction caches

        # Log file for debugging
        self.logfile = os.path.join(os.getcwd(),'X86.log')
        
        
        # Architecture details (not measured)
        self.instruction_caches = {}  # e.g., {'l1' : {'size': (32,'KB'), 'line_size': (64,'bytes'), 'associativity':'8-way set associative'}
        self.data_caches = {} # similar to data caches
        self.os_info = {} # e.g., {'os_name': 'Linux', 'os_release' : '2.6.35-28-generic'} etc.
        self.tlb = {}  # similar to caches
        self.memory = {} # e.g., {'total_size': (16080.64,'MB')}
        self.processors = {} # e.g., {'processors': 8, 'brand' : 'Intel Xeon', 'model' : 'E5462', 'clock_speed': (2799.51,'MHz')}

        # The number of time to run the experiment for each measurement
        #self.reps = 5
        pass


    def runBenchmark(self, cmd):
        # TODO: run entire benchmark 
        return

    def get_papi_avail_caller(self, **kwargs):
        '''if papi is on a machine, then it will help gather the data'''
        cmd = self.papi_path
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file = self.logfile)
        #will need to parse output, store it and make sure the naming is standardized
        return

    def get_hardware_specs(self, **kwargs):
        '''try multiple commands and gather hardware information'''
        #hardware_commands - assume linux queries will work on x86 system
        hardware_cache_sizes = 'lscpu'
        hardware_os = 'uname -a'
        hardware_total_mem = 'grep MemTotal /proc/meminfo'
        hardware_cpu_count = 'nproc'

        #get the number of processors
        self._log(hardware_cpu_count)
        return_code, cmd_output = system_or_die(hardware_cpu_count, log_file = self.logfile)
        cmd_output = int(cmd_output) 
        self.processors['processors']= cmd_output

        #extract all useful data out of lscpu
        self._log(hardware_cache_sizes)
        return_code, cmd_output = system_or_die(hardware_cache_sizes, log_file = self.logfile)
        
        for line in cmd_output.split(os.linesep):
            line = line.split(':')
            if(len(line) > 1):
                line[1] = line[1].strip()

            if(line[0].find('MHz') > 0):
                self.processors['clock_speed'] = float(line[1])

            if(line[0].find('cache') > 0):
                big = {}
                cache_type = line[0].split()
                if(cache_type[0].find('i') > 0):
                    vals = cache_type[0].split('i')
                    big['size'] = line[1]
                    self.instruction_caches[vals[0]] = big
                else:
                    vals = cache_type[0].split('d')
                    big['size'] = line[1]
                    self.data_caches[vals[0]] = big

        #extract all useful data out of uname -a
        self._log(hardware_os)
        return_code, cmd_output = system_or_die(hardware_os, log_file = self.logfile)

        cmd_output = cmd_output.split()
        self.os_info['os_name'] = cmd_output[0]
        self.os_info['os_release'] = cmd_output[2]
        print self.os_info

        #get hardware memory size from /proc/meminfo
        self._log(hardware_total_mem)
        return_code, cmd_output = system_or_die(hardware_total_mem, log_file = self.logfile)
        cmd_output = cmd_output.split(':')
        cmd_output[1] = cmd_output[1].strip()
        cmd_output = cmd_output[1].split()
        cmd_output[0] = float(cmd_output[0])
        self.memory['total_size'] =  cmd_output
        print self.memory
        return
               
                

    def get_mem_read_bw(self, **kwargs): 
        ''' Memory read bandwidth measurement with lmbench '''
        size = kwargs.get('size')
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        cmd = self.lmbench_path + 'bw_mem -P %s %s rd' % (procs,size)

        vals = []
        self._log(cmd)
        for i in range(0,int(reps)):
            """number of repetitions added as a parameter"""
            return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
            s,val = cmd_output.split()
            vals.append(float(val))
             
        params = {'metric':'mem_read_bw','size':s,'procs':procs,'reps':reps}
        self._recordMeasurement(params, Measurement(get_stats(vals),units='MB/s',params=params))
        return

    def get_l1_read_latency(self, procs=1,reps=1):
        ''' Measure L1 read latency and record in self.measurements. '''
        return self._get_read_latency(level=1, procs=procs, reps=reps)
    
    def get_l2_read_latency(self, procs=1,reps=1):
        ''' Measure L2 read latency and record in self.measurements. '''
        return self._get_read_latency(level=2, procs=procs,reps=reps)
    
    # TODO: add l3 function, but must check first whether machine has L3
    
    def get_mem_read_latency(self, procs=1,reps=1):
        ''' Measure memory read latency and record in self.measurements. '''
        return self._get_read_latency(level=3, procs=procs, reps=reps)

    def get_mem_write_bw(self, **kwargs):
        ''' Memory write bandwidth measurement with lmbench '''
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        start = int(kwargs.get('size'))
        self.get_bw('mem_write_bw', procs=procs, size=start, next_size=start, reps=reps, bw_type='wr') 
        return
    
    def get_l1_write_bw(self, **kwargs):
        ''' Measure L1 write bandwidth and record in self.measurements. '''
        self
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        
        #depending on size (which one you're looking for) can start around that range
        start = int(kwargs.get('size'))
        end = int(kwargs.get('next_size'))
        self.get_bw('l1_write_bw', procs=procs, size=start, next_size=end, reps=reps, bw_type='wr') 
        return
    
    def get_bw(self, **kwargs):
        ''' Measure L1 read bandwidth and record in self.measurements. '''
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        bw_type = kwargs.get('bw_type')
        #depending on size (which one you're looking for) can start around that range
        start = int(kwargs.get('size'))
        end = int(kwargs.get('next_size'))

        #have a max in case findjump returns empty
        max_means = -1 
        means = []
        stat_collector = { }

        for x in range(start, end):
            vals = []
            cmd = self.lmbench_path + 'bw_mem -P %s %s %s' % (procs, str(x)+'m', bw_type)
            self._log(cmd)
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
            
            if(value_to_jump > max_means):
                max_means = value_to_jump[0]
            
  
        #get the jump location in the range
        #what do you do if the jump is not in the range???
        getback = self.findjump(means)
        if(len(getback) == 1):
            track = getback[0]
        else:
            track = max_means

        mem_size = 0
        best = []
        
        #find final answers by looking through stat_collector
        for k, v in stat_collector.iteritems():
            #print "track: %s and v[0]: %s " % (track, v[0])
            if (v[0] == track):
                best = v
                mem_size = k

        #process vals 
        print best
        params = {'metric':'l1_read_bw','size':str(mem_size)+'m','procs':procs,'reps':reps}
        self._recordMeasurement(params, Measurement(best,units='MB/s',params=params))

        return


    #-------- private methods ------------------------------------
    
    def findjump(self, array):
        '''should find all jumps in a data set'''
        jumps = []
        counter = 0;
        min_mem = 256
        climb = False
        tolerance = 5 #may need to be a given depending on 
        
        #get differences between values to find biggest jump
        for i in range(0, len(array)):
            if(i+1 < len(array)):
                distance = float(abs(array[i+1] - array[i]))
               
                #possibly a jump
                if(distance > tolerance):
                    counter+=1

                    #distances are wobbly - not on a memory plateau
                    if(counter > 3): 
                        climb = True
                    #only store jumps if not climbing
                    if(not climb):
                        jumps.append(array[i])

                #should mean you are on a memory plateau
                else:
                    counter = 0
                    climb = False
                    
        #check that all recorded jumps are at least min mem dist
        for i in range(0, len(jumps)):
            if(i+1 < len(jumps)):
                dist = abs(jumps[i+1] - jumps[i])
                if(dist < min_mem):
                    #recorded a climb value rather than jump
                    del jumps[i+1]
       
        return jumps
    

    def _get_read_latency(self, level=1, procs=1, reps=1):
        ''' Measure L1 read latency and record in self.measurements. '''
        if level>0: memindex = level - 1
        else: memindex = level      # last level is indicated by -1
                
        # If we have already computed all latencies, just return the value
        if len(self.datalatency) >= level:
            return self.datalatency[memindex]

        if level > self.memory_levels:
            raise MeasurementException('Unrecognized memory level: %s (maximum levels = %d)' \
                                       % (str(level),self.memory_levels))
        cmd = self.lmbench_path + 'lat_mem_rd -P %s -N 1 %s %s' \
              % (str(procs), '256M', '256')

        self._log(cmd)
        #get output
        return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)

        sizes = []
        latencies = []   #  time in ns
                
        for line in cmd_output.split(os.linesep)[1:]:
            if not line: continue
            # process all lines except the first (which is just the size of the jump 
            val1, val2 = line.split()           # the format is "number number"
            # val1 is the log2(array_size) and val2 is time in nanoseconds
            sizes.append(float(val1)*1024.0)
            latencies.append(float(val2))  # size of test array in KB, time in ns


        #need to find the latency for the correct level (find jump)
        counter = 0
        relative_tolerance = 2.0 # TODO: make this a parameter in config
        old_i = 0
        
        #get differences between values to find biggest jump
        if len(latencies) < 2: 
            warn('Could not compute data read latencies at different memory levels')
            return
        for i in range(2,len(sizes),2):
            distance = float(latencies[i]) / float(latencies[i-2]) 
            if distance > relative_tolerance:
                #print 'Found jump: ', counter+1, distance, latencies[i-1], old_i, i
                # detected a jump
                counter += 1
                 
                # the name of the metric
                name = 'l' + str(counter) + '_read_latency'
                
                params = {'metric':name,'size':str(sizes[i-1])+'KB','procs':procs,'reps':reps}
                mes = Measurement(get_stats(latencies[old_i+2:i-2]),units='ns',params=params)
                self._recordMeasurement(params, mes)
                self.datalatency.append(mes)
                old_i = i + 1
                # Skip the smaller sizes in the next level
                if i < len(sizes)-3: i += 3

            if counter > self.memory_levels: break  
        
        # Record the last level (memory)
        counter += 1
        params = {'metric':'mem_read_latency','size':str(sizes[i-1])+'KB','procs':procs,'reps':reps}
        # Skip some of the smaller memory values since they are not indicative of larger sizes
        mes = Measurement(get_stats(latencies[old_i+8:]),units='ns',params=params)
        self._recordMeasurement(params, mes)
        self.datalatency.append(mes)

        if len(self.datalatency) < level:
            warn('Could not compute data for memory level', level)
            return None
        
        return self.datalatency[memindex]
        

    def _log(self, thestr):
        f = open(self.logfile,"a")
        f.write("%s\n" % thestr)
        f.close()

    def _recordMeasurement(self, params, measurement):
        ''' Record the measurement and relevant parameters in the log file. '''
        key = str(params)
        self.measurements[key] = measurement
        f = open(self.logfile,"a")
        f.write("%s\n" % str(self.measurements[key]))
        f.close()
