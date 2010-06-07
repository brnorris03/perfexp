import ConfigParser

class Params():

    def __init__(self):
        
        global DEBUG
        global workdir
        global mpidir
        global cmdline
        global cmdlineopts
        global threads
        global processes
        global nodes
        global tasks_per_node
        global pmodel
        global instrumentation
        global exemode
        global batchcmd
        global jobname
        global walltime
        global maxprocessor
        global accountname
        global buffersize
        global msgsize
        global stacksize
        global counters   
        
        
    def _processConfigFile(self):
        
        mysection = 'ExperimentDriver'
        self.config = ConfigParser.ConfigParser()
        self.config_file = 'src/examples/params.txt'
        self.config.readfp(open(self.config_file))
        
        try:
            DEBUG = self.config.get(mysection, 'DEBUG')
        
        except:
            raise Exception('Error: could not find DEBUG in configuration file %s' % self.config_file)

        try:
            workdir = self.config.get(mysection, 'workdir')
        
        except:
            raise Exception('Error: could not find workdir in configuration file %s' % self.config_file)

        try:
            mpidir = self.config.get(mysection, 'mpidir')
        
        except:
            raise Exception('Error: could not find mpidir in configuration file %s' % self.config_file)

        try:
            cmdline = self.config.get(mysection, 'cmdline')
        
        except:
            raise Exception('Error: could not find cmdline in configuration file %s' % self.config_file)

        try:
            cmdlineopts = self.config.get(mysection, 'cmdlineopts')
        
        except:
            raise Exception('Error: could not find cmdlineopts in configuration file %s' % self.config_file)

        try:
            threads = self.config.get(mysection, 'threads')
        
        except:
            raise Exception('Error: could not find threads in configuration file %s' % self.config_file)


        try:
            processes = self.config.get(mysection, 'processes')
        
        except:
            raise Exception('Error: could not find processes in configuration file %s' % self.config_file)

        try:
            nodes = self.config.get(mysection, 'nodes')
        
        except:
            raise Exception('Error: could not find nodes in configuration file %s' % self.config_file)

        try:
            tasks_per_node = self.config.get(mysection, 'tasks_per_node')
        
        except:
            raise Exception('Error: could not find tasks_per_node in configuration file %s' % self.config_file)

        try:
            pmodel = self.config.get(mysection, 'pmodel')
        
        except:
            raise Exception('Error: could not find pmodel in configuration file %s' % self.config_file)

        try:
            instrumentation = self.config.get(mysection, 'instrumentation')
        
        except:
            raise Exception('Error: could not find instrumentation in configuration file %s' % self.config_file)

        try:
            exemode = self.config.get(mysection, 'exemode')
        
        except:
            raise Exception('Error: could not find exemode in configuration file %s' % self.config_file)

        try:
            batchcmd = self.config.get(mysection, 'batchcmd')
        
        except:
            raise Exception('Error: could not find batchcmd in configuration file %s' % self.config_file)


        try:
            jobname = self.config.get(mysection, 'jobname')
        
        except:
            raise Exception('Error: could not find jobname in configuration file %s' % self.config_file)

        try:
            walltime = self.config.get(mysection, 'walltime')
        
        except:
            raise Exception('Error: could not find walltime in configuration file %s' % self.config_file)

        try:
            maxprocessor = self.config.get(mysection, 'maxprocessor')
        
        except:
            raise Exception('Error: could not find maxprocessor in configuration file %s' % self.config_file)

        try:
            accountname = self.config.get(mysection, 'accountname')
        
        except:
            raise Exception('Error: could not find accountname in configuration file %s' % self.config_file)

        try:
            buffersize = self.config.get(mysection, 'buffersize')
        
        except:
            raise Exception('Error: could not find buffersize in configuration file %s' % self.config_file)

        try:
            msgsize = self.config.get(mysection, 'msgsize')
        
        except:
            raise Exception('Error: could not find msgsize in configuration file %s' % self.config_file)

        try:
            stacksize = self.config.get(mysection, 'stacksize')
        
        except:
            raise Exception('Error: could not find stacksize in configuration file %s' % self.config_file)


        try:
            counters = self.config.get(mysection, 'counters')
        
        except:
            raise Exception('Error: could not find counters in configuration file %s' % self.config_file)






