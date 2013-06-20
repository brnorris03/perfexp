from sys import float_info

class AbstractPlatform:
    def __init__(self):
        ''' 
        Store measurements in a dictionary whose keys are the names of 
        metrics, and each value values is an instance of the Measurement class
        '''

        self.memory_metrics = []
        for memlevel in ['mem', 'l1', 'l2', 'l3']:
            for metric in ['read_latency', 'read_bw', 'write_latency', 'write_bw', 'rw_latency', 'rw_bw']:
                self.memory_metrics.append('%s_%s' % (memlevel, metric))

        self.measurements = {}

    def help(self):
        print 'Available metrics: '
        print self.memory_metrics
        if self.measurements: print self.measurements

    def runBenchmark(self, cmd):
        ''' 
        For benchmarks that collect a lot of data at once, implement and use this method.
        - cmd: The command to the benchmarks executable, including arguments.
        '''
        raise NotImplementedError
    
    def measure(self, metric, **kwargs):
        '''
        Measure a single metric on the current architecture.
        - metric: The string name of the metric to be measured
        - kwargs: keyword arguments to pass to specific function
        This method dispatches to the appropriate function.
        '''
        methodname = 'self.get_' + metric + '(**kwargs)'
        eval(methodname)
        return

    def get_mem_read_latency(self, **kwargs):
        ''' Measure memory read latency and record in self.measurements. '''
        raise NotImplementedError

    def get_mem_read_bw(self, **kwargs):
        ''' Measure memory read bandwidth  and record in self.measurements. '''
        raise NotImplementedError

    def get_l1_read_latency(self, **kwargs):
        ''' Measure L1 read latency and record in self.measurements. '''
        raise NotImplementedError

    def get_l1_read_bw(self, **kwargs):
        ''' Measure L1 read bandwidth and record in self.measurements. '''
        raise NotImplementedError



class Measurement:
    def __init__(self, stats, units, params=[]):
        self.mean = stats[0]
        self.min = stats[1]
        self.max = stats[2]
        self.units = units
        self.params = params

    def __repr__(self):
        ''' print object contents '''
        return "%s: {'mean':%s,'min':%s,'max':%s,'units':%s}"  \
            % (str(self.params), str(self.mean),str(self.min),str(self.max),self.units)