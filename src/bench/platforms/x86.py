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
        self.blackjack_caches_path = '/homes/kachalas/blackjack/trunk/Cache_Discovery_Benchmakrs'
        self.blackjack_liverange_path = '/homes/kachalas/blackjack/trunk/LiveRange'
        #others couldn't get makefile to work right  and core count fails

        # TODO change 4 to the actual number of memory levels (incl. caches and main memory)
        self.memory_levels = 3
        # The number of time to run the experiment for each measurement
        self.reps = 2


        #get cache details and store here
        self.rd_data_bw = {}
        self.wr_data_bw = {}
        self.cp_data_bw = {}
        self.blackjack_cache_details = {}

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
        # fill architecture details
        self.get_hardware_specs() # gathers hardware intel 

        #self.fillbw()
        #print self.cp_data_bw
        pass


    def runBenchmark(self, cmd):
        # TODO: run entire benchmark 
        return

    def get_blackjack_avail_caller(self, **kwargs):
        '''if blackjack in on a machine, can run this method'''
        #cmd = 'cd '+self.blackjack_caches_path+' && make'
        #apparently bellow cmd doesn't work on solaris 10, AIX, or HP-UX 11.23
        cmd = 'make -C ' + self.blackjack_caches_path  
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file = self.logfile)
    
        latFlag = False
        latcounter = 0
        
        for line in cmd_output.split(os.linesep):
            if(len(line) > 1):
                
                if(line.find('==>') >= 0):
                    line = line.split('==>')
                    line = line[1]
                    #flag the start of cache size and latencies
                    if(line.find('sizes and latencies are') >= 0):
                        latFlag = True
                        latcounter = 1
                    #handling the associativity
                    elif(line.find('associativity') >= 0):
                        line = line.split(':')
                        line[0] = line[0].strip()
                        self.blackjack_cache_details[line[0]] = int(line[1])
                    #handling the line size
                    elif(line.find('cache line') >= 0):
                        temp = []
                        line = line.split(':')
                        line[0] = line[0].strip()
                        temp = line[1].split()
                        self.blackjack_cache_details[line[0]] = temp
                        

                #handling the latency/cache sizes 
                elif(latcounter > 0):
                    if((line.find('raw file') >= 0) and latFlag):
                        latFlag = False
                        #last level is likely memory rather than cache
                        lvl = 'L' + str(latcounter-1)
                        mem = self.blackjack_cache_details[lvl]
                        del self.blackjack_cache_details[lvl]
                        self.blackjack_cache_details['mem'] = mem
                        latcounter = -1
                    if(latFlag):
                        temp = {}
                        line = line.split()
                        vals = [float(line[0]), 'KiB']
                        temp['size'] = vals
                        vals = [float(line[1]), 'ns']
                        temp['latency'] = vals
                        self.blackjack_cache_details['L'+str(latcounter)] = temp 
                        latcounter+=1        
                
        #liveranges benchmarks called from blackjack
        cmd = 'make -C '+self.blackjack_liverange_path
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file = self.logfile)
        #parse output
        flag = False
        for line in cmd_output.split(os.linesep):
            if(len(line) > 1):
                if(line.find('Running the Live Range') >= 0):
                    flag = True
                if(line.find('Leaving') >= 0):
                    flag = False
                if(flag):
                    if(line.find('/') >= 0):
                        #found place in code
                        print line
                        #storing bizarre results (unknown reason)
                        self.blackjack_cache_details['live ranges'] = line
                        break
                        
        return
        

    def get_papi_avail_caller(self, **kwargs):
        '''if papi is on a machine, then it will help gather the data'''
        cmd = self.papi_path
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file = self.logfile)
        
        # parsed output for model and brand
        for line in cmd_output.split(os.linesep):
            line = line.split(':')
           
            if(len(line) > 1):
                #get model information and self store
                if(line[0].find('Model') >= 0):
                    line = line[1].split('CPU')
                    line[0] = line[0].lstrip()
                    line[0] = line[0].rstrip()
                    self.processors['brand'] = line[0]
                    line = line[1].split('@')
                    line = line[0].strip()
                    self.processors['model'] = line
                if(line[0].find('Hdw Threads') >= 0):
                    self.processors['hdw_threads_per_core']= int(line[1])
                if(line[0].find('CPUs per Node') >= 0):
                    self.processors['CPUs_per_node'] = line[1]
                
        print self.processors
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
        
        #getting the vendor info
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
        

        #get hardware memory size from /proc/meminfo
        self._log(hardware_total_mem)
        return_code, cmd_output = system_or_die(hardware_total_mem, log_file = self.logfile)
        cmd_output = cmd_output.split(':')
        cmd_output[1] = cmd_output[1].strip()
        cmd_output = cmd_output[1].split()
        cmd_output[0] = float(cmd_output[0])
        self.memory['total_size'] =  cmd_output
        
        #calls to other benchmarks
        self.get_papi_avail_caller()
        #self.get_blackjack_avail_caller()
        return
               

    def get_l1_read_latency(self, procs=1,reps=1):
        ''' Measure L1 read latency and record in self.measurements. '''
        return self._get_read_latency(level=1, procs=procs, reps=reps)
    
    def get_l2_read_latency(self, procs=1,reps=1):
        ''' Measure L2 read latency and record in self.measurements. '''
        return self._get_read_latency(level=2, procs=procs,reps=reps)
    
    def get_l3_read_latency(self, procs=1,reps=2):
        '''Measure L3 read latency if l3 cache exists and record in self.measurements'''      
        if('L3' in self.data_caches):
            return self.get_read_latency(level=3, procs=procs,reps=reps)
        else:
            return 'ERROR: No L3 cache'
    
    def get_mem_read_latency(self, procs=1,reps=1):
        ''' Measure memory read latency and record in self.measurements. '''
        if('L3' in self.data_caches):
            return self._get_read_latency(level=4, procs=procs, reps=reps)
        else:
            return self._get_read_latency(level=3, procs=procs, reps=reps)


    def get_mem_read_bw(self, **kwargs): 
        ''' Memory read bandwidth measurement with lmbench '''
        start = int(kwargs.get('size'))
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        gran = kwargs.get('gran')
        self.get_bw(memo='mem_read_bw', procs = procs, size=start, next_size=start, gran=gran, reps=reps, bw_type='rd')
        return

    def get_l1_read_bw(self, **kwargs):
        ''' Measure L1 read bandwidth and record in self.measurements. '''
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        #range of l1 cache size - can be acquired from hardware specs
        start = int(kwargs.get('size'))
        end = int(kwargs.get('next_size'))
        gran = kwargs.get('gran')
        self.get_bw('l1_read_bw', procs=procs, size=start, next_size=end, gran=gran, reps=reps, bw_type='rd') 
        return

    def get_l2_read_bw(self, **kwargs):
        ''' Measure L2 read bandwidth and record in self.measurements. '''
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        #range of l2 cache size
        start = int(kwargs.get('size'))
        end = int(kwargs.get('next_size'))
        gran = kwargs.get('gran')
        #call bandwidth method
        self.get_bw(memo='l2_read_bw', procs=procs, size=start, next_size=end, gran=gran, reps=reps, bw_type='rd') 
        return

    def get_mem_write_bw(self, **kwargs):
        ''' Memory write bandwidth measurement with lmbench '''
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        start = int(kwargs.get('size'))
        gran = kwargs.get('gran')
        self.get_bw(memo='mem_write_bw', procs=procs, size=start, next_size=start, gran=gran, reps=reps, bw_type='wr') 
        return
    
    def get_l1_write_bw(self, **kwargs):
        ''' Measure L1 write bandwidth and record in self.measurements. '''
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        #range of l1 cache size
        start = int(kwargs.get('size'))
        end = int(kwargs.get('next_size'))
        gran = kwargs.get('gran')
        self.get_bw(memo='l1_write_bw', procs=procs, size=start, next_size=end, gran=gran, reps=reps, bw_type='wr') 
        return

    def get_l2_write_bw(self, **kwargs):
        ''' Measure L2 write bandwidth and record in self.measurements. '''
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        #range of l2 cache size
        start = int(kwargs.get('size'))
        end = int(kwargs.get('next_size'))
        gran = kwargs.get('gran')
        #call bandwidth method
        self.get_bw(memo='l2_write_bw', procs=procs, size=start, next_size=end, gran=gran, reps=reps, bw_type='wr') 
        return
    
    def get_bw(self, **kwargs):
        ''' Measure bandwidth and record in self.measurements. '''
        memo = kwargs.get('memo')
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        bw_type = kwargs.get('bw_type')
        #depending on size (which one you're looking for) can start around that range
        start = int(kwargs.get('size'))
        end = int(kwargs.get('next_size'))
        gran = kwargs.get('gran')
        #have a max in case findjump returns empty
        max_means = -1 
        means = []
        stat_collector = { }

        for x in range(start, end):
            vals = []
            cmd = self.lmbench_path + 'bw_mem -P %s %s %s' % (procs, str(x)+gran, bw_type)
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
        print getback
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
        params = {'metric':memo,'size':str(mem_size)+'m','procs':procs,'reps':reps}
        self._recordMeasurement(params, Measurement(best,units='MB/s',params=params))

        return track


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
        
    def fillbw(self, **kwargs):
        #zone is how much above and below memory size to check
        zone = 3
        #get bw for main memory
        big = self.memory['total_size']
        big[0] = big[0]/1000
        #self.rd_data_bw['mem'] = self.get_bw(memo='mem_read_bw', procs=1, size=(big[0]-zone), next_size=(big[0]+zone), gran='m',reps=self.reps, bw_type='rd')
        #self.wr_data_bw['mem'] = self.get_bw(memo='mem_write_bw', procs=1, size=(big[0]-zone), next_size=(big[0]+zone), gran='m',reps=self.reps, bw_type='wr')
        #self.cp_data_bw['mem'] = self.get_bw(memo='mem_copy_bw', procs=1, size=(big[0]-zone), next_size=(big[0]+zone), gran='m',reps=self.reps, bw_type='cp')
        #should get the correct bws for the levels of memory
        for k,v in self.data_caches.iteritems():
            #get k into form
            k = k.lower()
            #get correct sizes
            v=v['size'].lower()
            v, em = v.split('k')
            v = int(v)
            #populate arrays with levels of cache in corresponding cells
            self.rd_data_bw[k] = self.get_bw(memo=k+'_read_bw', procs=1, size=(v-zone), next_size=(v+zone), gran='k',reps=self.reps, bw_type='rd')
            self.wr_data_bw[k] = self.get_bw(memo=k+'_write_bw', procs=1, size=(v-zone), next_size=(v+zone), gran='k',reps=self.reps, bw_type='wr')
            self.cp_data_bw[k] = self.get_bw(memo=k+'_copy_bw', procs=1, size=(v-zone), next_size=(v+zone), gran='k',reps=self.reps, bw_type='cp')
        return

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
