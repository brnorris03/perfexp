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
        self.papi_path = '/disks/soft/papi-4.4.0/bin/'
        self.perfsuite_path = '/disks/large/soft/perfsuite-1.1.0/bin/'
        self.ior_path = '/homes/kachalas/ior/src/'
        self.blackjack_path = '/homes/kachalas/blackjack/trunk/'
        #others couldn't get makefile to work right  and core count fails

        # TODO change 4 to the actual number of memory levels (incl. caches and main memory)
        self.memory_levels = 3
        # The number of time to run the experiment for each measurement
        self.reps = 2


        #get cache details and store here
        self.rd_data_bw = {}
        self.wr_data_bw = {}
        self.cp_data_bw = {}

        # BENCHMARK-GATHERED DETAILS
        # BLACKJACK
        self.blackjack_cache_details = {}
        # LMBENCH
        self.lmbench_cache_details = {}
        self.lmbench_basic_proc_ops = {}
        self.lmbench_create_delete = {}
        self.lmbench_pipe = {}
        #PERFSUITE
        self.perfsuite_cache = []
        self.perfsuite_tlb = []
        self.perfsuite_system = []
        self.perfsuite_processor = []
        #PAPI
        self.papi_hdw_info = {}
        self.papi_hdw_counters = {}
        self.papi_native = []
        self.papi_total_events = ''
        #IOR
        self.ior_runtimes = {}


        # An array of Measurement objects for each level of the memory hierarchy
        # starting with L1
        self.datalatency = []  # data caches and main memory
        self.instrlatency = []  # instruction caches
        self.network_latency = {} #network latencies for diff kinds of protocols
        self.system_ovrhds = {}

        # Log file for debugging
        self.logfile = os.path.join(os.getcwd(),'X86.log')
        
        
        # Architecture details (not measured)
        self.instruction_caches = {}  # e.g., {'l1' : {'size': (32,'KB'), 'line_size': (64,'bytes'), 'associativity':'8-way set associative'}
        self.data_caches = {} # similar to data caches
        self.os_info = {} # e.g., {'os_name': 'Linux', 'os_release' : '2.6.35-28-generic'} etc.
        self.tlb = {}  # similar to caches
        self.memory = {} # e.g., {'total_size': (16080.64,'MB')}
        self.processors = {} # e.g., {'processors': 8, 'brand' : 'Intel Xeon', 'model' : 'E5462', 'clock_speed': (2799.51,'MHz')}
       
        #run the benchmark - at least filling in the hardware details.
        self.runBenchmark('ok')
        
        pass


    def runBenchmark(self, cmd):
        self.get_hardware_specs()
        self.fillbw()
        #could possibly get an array of commands and run through them...
        # TODO: run entire benchmark 
        return

    def get_ior_avail_caller(self, **kwargs):
        reps = int(kwargs.get('reps'))
        ops = kwargs.get('options')
        cmd = self.ior_path + 'ior ' + ops
       
        for i in range(0, reps):
            self._log(cmd)
            return_code, cmd_output = system_or_die(cmd, log_file = self.logfile)
            seen_summary = False
            skip_line = False
            get_settings = False
            settings = {}
            hold = []
            rep_vals = {}
            for line in cmd_output.split(os.linesep):
                if(line.find('Summary of all') >= 0):
                    #place to get values
                    seen_summary = True
                    skip_line = True
                elif(line.find('Summary') >= 0):
                    #record settings for run's results
                    get_settings = True
                elif(get_settings):
                    if not line: 
                        get_settings = False
                    else:
                        line = line.split('=')
                        line[0] = line[0].strip()
                        settings[line[0]] = line[1].strip()
                elif(skip_line):
                    #this should be metrics
                    skip_line = False
                    line = line.split()
                    hold = line
                elif(seen_summary and line.find('Finished') < 0):
                    #store details of read and write
                    line = line.split()
                    for j in range(0,len(line)):
                        #should match up
                        rep_vals[hold[j]] = line[j]
                    temp = rep_vals
                    self.ior_runtimes['rep_' + str(i)+ '_'+ temp['Operation']] = temp 
                elif(line.find('Finished') >= 0):
                    self.ior_runtimes['rep_' + str(i)+'_end'] = line
                    temp = settings
                    self.ior_runtimes['rep_' + str(i)+'_settings'] = temp
                elif(line.find('started') >= 0):
                    self.ior_runtimes['rep_' + str(i)+'_start'] = line

        params = {'metric':cmd,'reps':reps}
        self._recordMeasurement(params, self.ior_runtimes)

        print self.ior_runtimes
        return


    def get_blackjack_avail_caller(self, **kwargs):
        '''if blackjack in on a machine, can run this method'''
        #cmd = 'cd '+self.blackjack_path +'Cache_Discovery_Benchmakrs && make'
        #apparently bellow cmd doesn't work on solaris 10, AIX, or HP-UX 11.23
        cmd = 'make -C ' + self.blackjack_path + 'Cache_Discovery_Benchmakrs'  
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
        cmd = 'make -C '+ self.blackjack_path + 'LiveRange'
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
        
    def get_perfsuite_avail_caller(self, **kwargs ):
        '''if perfsuite is on a machine, then it will help gather the data'''
        cmd = self.perfsuite_path + 'psinv'
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file = self.logfile)

        #PARSING
        initial_H = False
        overall_head = ''
        tracking = {}
        counter = 0
        accessory = 0
        full_list = []
        heading = ''
        level_dic = {}
        activate_count = False

        for line in cmd_output.split(os.linesep):
            if not line: continue
            if((line.find('Information -') > -1) or (line.find('Details -') > -1)):
                #store info of a full list
                if(initial_H):
                    kind = overall_head
                    tracking['kind'] = kind
                    life_within = tracking
                    #alias lists
                    if(kind.find('System Information') >= 0 or kind.find('TLB Information') >= 0):
                        full_list = self.perfsuite_system
                    elif(kind.find('Processor Information') >= 0):
                        full_list = self.perfsuite_processor
                    else:
                        full_list = self.perfsuite_cache
                    
                    full_list.append(life_within)

                    #restart list
                    tracking = {}    
           
                line = line.split('-')
                overall_head = line[0].strip()
                #prevents storing empty list and mismatches
                initial_H = True

            elif(line.find(':') >= 0):
                #info to store
                line = line.split(':')
                line[1] = line[1].strip()
                line[0] = line[0].strip('\t\n\r')
                
                #formatted like a level
                if not line[1]:
                    #store and clear lvl list
                    if(activate_count):
                        val = heading
                        vals = level_dic
                        tracking[val] = vals
                        level_dic = {}

                    counter = 0
                    accessory = 0
                    activate_count = True
                    heading = line[0]
                   
                else:
                    if(activate_count):
                        counter += 1
                        val = line[0]+'_'+str(accessory)
                        level_dic[val] = [line[1]]
                        #every four is a different set
                        if(counter == 4):
                            accessory += 1
                            counter = 0
                    else:
                        #no separate levels
                        tracking[line[0]] = [line[1]]
        
        #the last list should be the one left over after loop
        tracking['kind'] = overall_head
        tracking[heading] = level_dic
        full_list = self.perfsuite_tlb
        full_list.append(tracking)


        return

    def get_papi_avail_caller(self, **kwargs):
        '''if papi is on a machine, then it will help gather the data'''
        cmd = self.papi_path + 'papi_avail -a'
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file = self.logfile)
        
        counter = 0
        # parsed output for model and brand
        for line in cmd_output.split(os.linesep):
            if not line: continue
            
            #get model information and self store
            if(line.find('--------') >= 0):
                counter+=1

            if(counter == 2):
                line = line.split()
                if(line[0].find('PAPI') >= 0):
                    self.papi_hdw_counters[line[0]] = ' '.join(line[3:])
    
            else:
                line = line.split(':')
                line[0]=line[0].strip()
                if(len(line) > 2):
                    format_1 = line[2].split()
                    format_2 = line[3].split()
                    val = {}
                    print line
                    val[line[1]]=format_1[0].strip()
                    val[format_1[1]]=format_2[0].strip()
                    val[format_2[1]]=line[4].strip()
                    self.papi_hdw_info[line[0]]=val
                else:
                    if(len(line) >= 2):
                        self.papi_hdw_info[line[0]]=line[1].strip()

        cmd = self.papi_path + 'papi_native_avail'
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file = self.logfile)

        check_next = False
        for line in cmd_output.split(os.linesep)[20:]:
            if not line: continue
            if(line.find('Total events') >= 0):
                line = line.split(':')
                self.papi_total_events = line[1]
            elif(line.find('----------------') >= 0):
                check_next = True
            else:
                if(check_next == True):
                    line = line.split('|')
                    if(len(line) >= 2):
                        self.papi_native.append(line[1].strip())
                        check_next = False

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

    def get_process_creation(self, **kwargs):
        ''' Measure process creation times in self.measurements. '''
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        
        #different processes to try
        processes = ['procedure', 'fork', 'exec']
        stat_collector = { }

        for proc in processes:
            vals = []
            cmd = self.lmbench_path + 'lat_proc -P %s %s' % (procs, proc)
            self._log(cmd)
            
            for i in range(0,int(reps)):
                """number of repetitions added as a parameter"""
                return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
                if(cmd_output.find('Procedure') >= 0 or cmd_output.find('Process') >= 0):
                    part=cmd_output.split()
                    vals.append(float(part[2]))
                
            #keep statistics to pass
            stat_collector[proc] = vals
        
        #do shell separately - different output
        cmd = self.lmbench_path + 'lat_proc -P %s %s' % (procs, 'shell')
        self._log(cmd)
        vals = []
        for i in range(0,int(reps)):
            return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
            for line in cmd_output.split(os.linesep):
                if(line.find('Process') >= 0):
                    line = line.split()
                    vals.append(float(line[3]))
        stat_collector['shell']=vals
            
        #record answers
        for k, v in stat_collector.iteritems():
            #record all metrics
            params = {'metric':'lat_proc_'+k,'procs':procs,'reps':reps}
            self._recordMeasurement(params, Measurement(get_stats(v),units='micoseconds',params=params))
    
        return 


    def get_context_switches(self, **kwargs):
        ''' Measure context switching with lat_ctx in lmbench in self.measurements. '''
        procs = kwargs.get('procs')
        size = kwargs.get('size')
        reps = kwargs.get('reps')
        contxts = kwargs.get('contexts')
        cmd = self.lmbench_path + 'lat_ctx -P %s -N %s -s %s ' % (procs, reps, size)
        cmd = cmd + contxts
        self._log(cmd)
        
        return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
        collect_output = {}
        for line in cmd_output.split(os.linesep)[1:]:
            if not line: continue
            if(line.find('ovr') >= 0):
                line = line.split('=')
                val = len(line)-1
                collect_output['overhead'] = float(line[val])
            else:
                val1, val2 = line.split()          
                # val1 is the context and val2 is time in nanoseconds
                collect_output[int(val1)] = float(val2)

        params = {'metric':'lat_ctx','procs':procs,'size':size, 'contexts':contxts}
        self._recordMeasurement(params, collect_output)
        return

    def get_syscall_ovrhds(self, **kwargs):
        '''get overheads for OS calls'''
        fd = kwargs.get('test_open')
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        calls = ['null', 'read', 'write', 'stat', 'fstat','open']

        for call in calls:
            if(call == 'open'):
                if(fd != ""):
                    cmd = self.lmbench_path + 'lat_syscall -P %s -N %s open %s' % (procs, reps, fd)
                else:
                    print 'Error on open file test - file not specified'
            else:
                cmd = self.lmbench_path + 'lat_syscall -P %s -N %s %s' % (procs, reps, call)
            self._log(cmd)
            return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
            for line in cmd_output.split(os.linesep):
                if not line: continue
                line = line.split(":")
                line = line[1].split()
                self.system_ovrhds[call] = [float(line[0]), 'microseconds']
                
        params = {'metric':'lat_syscall','procs':procs,'reps':reps, 'calls':calls}
        self._recordMeasurement(params, self.system_ovrhds)
        return

    def get_network_latency(self, **kwargs):
        '''get network latency values '''
        message = kwargs.get('msg_size')
        procs = kwargs.get('procs')
        reps = kwargs.get('reps')
        #can be udp or tcp
        lat_type = kwargs.get('lat_type')
        #server and, client or shutdown
        server = kwargs.get('server')
        client = kwargs.get('comm')
        
        #create command
        cmd_binder = cmd = self.lmbench_path + 'lat_' + lat_type + ' '
        if message:  
            cmd_binder += '-m %s ' % (message)
            cmd += '-m %s ' % (message)
        
        #server specified
        if not server:
            cmd_binder += '-P %s -N %s -s' % (procs, reps)
        else:
            cmd_binder += '-P %s -N %s -S %s' % (procs, reps, server)
        self._log(cmd_binder) 
        return_code, cmd_output = system_or_die(cmd_binder, log_file=self.logfile)
        
        #client or shutdown specified (shutdown needs to have a minus input
        cmd += '-P %s -N %s %s' % (procs, reps, client)
        self._log(cmd) 
        return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
        
        for line in cmd_output.split(os.linesep):
            if not line: continue
            line = line.split(':')
            line = line[1].split()
            self.network_latency[lat_type] = [float(line[0]), 'microseconds'] 

       
        params = {'metric':'lat_'+lat_type,'procs':procs,'reps':reps, 'msg_size':message, 'server':server, 'client':client}
        self._recordMeasurement(params, self.network_latency)
        return

    def get_tlb(self, **kwargs):
        '''Gets the number of pages in the tlb '''
        reps = kwargs.get('reps')
        cmd = self.lmbench_path + 'tlb -N %s' % (reps)
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
        for line in cmd_output.split(os.linesep):
            if not line: continue
            line = line.split()
            self.tlb['pages']=int(line[1])
        
        return

    def get_cache_lmbench(self, **kwargs):
        '''Find the levels of cache and line sizes with lmbench cache call'''
        cmd = self.lmbench_path + 'cache'
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)
        for line in cmd_output.split(os.linesep):
            if not line: continue
            line = line.split(':')
            vals = line[1].split()
            if(line[0].find('Memory') < 0):
                self.lmbench_cache_details[line[0]]= {'size':[int(vals[0]), vals[1]], \
                                                          'latency':[float(vals[2]), vals[3]], \
                                                          vals[5]:[int(vals[4]),'bytes'], \
                                                          vals[7]:float(vals[6])}
            else:
                self.lmbench_cache_details[line[0]]={'latency':[float(vals[0]),vals[1]], \
                                                         vals[3]:float(vals[2])}

        return

    def get_cacheline_lmbench(self):
        '''Find the levels of cache line sizes with lmbench line call'''
        cmd = self.lmbench_path + 'line'
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)

        size = 0
        for line in cmd_output.split(os.linesep):
            if not line: continue
            size = line

        for k,v in self.data_caches.iteritems():
            v['linesize'] = [int(size), 'bytes']
        
        return

    def get_pipe_latency(self):
        '''Find the pipe latency'''
        cmd = self.lmbench_path + 'lat_pipe'
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)

        for line in cmd_output.split(os.linesep):
            if not line: continue
            line = line.split(':')
            val = line[1].split()
            self.lmbench_pipe[line[0]]=[float(val[0]), val[1]]
     
        return


    def get_pipe_bw(self):
        '''Find the pipe bandwidth'''
        cmd = self.lmbench_path + 'bw_pipe'
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)

        for line in cmd_output.split(os.linesep):
            if not line: continue
            line = line.split(':')
            val = line[1].split()
            self.lmbench_pipe[line[0]]=[float(val[0]), val[1]]
        print self.lmbench_pipe
        return

    def get_basic_proc_ops(self):
        '''Find latency for basic ops like int XOR,ADD,SUB,MUL,DIV,MOD'''
        cmd = self.lmbench_path + 'lat_ops'
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)

        for line in cmd_output.split(os.linesep):
            if not line: continue
            line = line.split(':')
            val = line[1].split()
            self.lmbench_basic_proc_ops[line[0]]=[float(val[0]), val[1]]
     
        return

    def get_create_delete_perf(self):
        '''Find file systems create and delete performance'''
        cmd = self.lmbench_path + 'lat_fs'
        self._log(cmd)
        return_code, cmd_output = system_or_die(cmd, log_file=self.logfile)

        for line in cmd_output.split(os.linesep):
            if not line: continue
            line = line.split()
            val = {'number created':int(line[1]), \
                       'creations/sec':int(line[2]), 'removals/sec':int(line[3])}
            self.lmbench_create_delete[line[0]] = val
     
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
