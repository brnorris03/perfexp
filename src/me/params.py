import ConfigParser
import os

class MEParams:

    meparams = {'DEBUG':None, 'workdir':None, 'mpidir':None, 'mpicmd':None, 'cmdline':None, 'threads':None, 'processes':None, 'nodes':None, 'tasks_per_node':None, 'pmodel':None, 'instrumentation':None, 'exemode':None, 'batchcmd':None, 'jobname':None, 'walltime':None, 'maxprocessor':None, 'accountname':None, 'buffersize':None, 'msgsize':None, 'stacksize':None, 'counters':None, 'commode':None}
	
    def _processConfigFile(self):
 
        mysection = 'ExperimentDriver'
        self.config = ConfigParser.ConfigParser()
        self.config_file = os.environ.get("PERFEXPDIR") + '/src/examples/params/params.txt'
        self.config.readfp(open(self.config_file))
        
        try:
            self.meparams['DEBUG'] = self.config.get('General', 'DEBUG')
        except:
            raise Exception('Error: could not find DEBUG in configuration file %s' % self.config_file)

        try:
            self.meparams['workdir'] = self.config.get(mysection, 'workdir')
        except:
            raise Exception('Error: could not find workdir in configuration file %s' % self.config_file)

        try:
            self.meparams['mpidir'] = self.config.get(mysection, 'mpidir')
        except:
            raise Exception('Error: could not find mpidir in configuration file %s' % self.config_file)

        try:
            self.meparams['mpicmd'] = self.config.get(mysection, 'mpicmd')
        except:
            raise Exception('Error: could not find mpicmd (e.g., mpicmd = mpiexec -np 4) in configuration file %s' % self.config_file)

        try:
            self.meparams['cmdline'] = self.config.get(mysection, 'cmdline')
        
        except:
            raise Exception('Error: could not find cmdline in configuration file %s' % self.config_file)

        try:
            self.meparams['threads'] = self.config.get(mysection, 'threads')
        
        except:
            raise Exception('Error: could not find threads in configuration file %s' % self.config_file)


        try:
            self.meparams['processes'] = self.config.get(mysection, 'processes')
        
        except:
            raise Exception('Error: could not find processes in configuration file %s' % self.config_file)

        try:
            self.meparams['nodes'] = self.config.get(mysection, 'nodes')
        
        except:
            raise Exception('Error: could not find nodes in configuration file %s' % self.config_file)

        try:
            self.meparams['tasks_per_node'] = self.config.get(mysection, 'tasks_per_node')
        
        except:
            raise Exception('Error: could not find tasks_per_node in configuration file %s' % self.config_file)

        try:
            self.meparams['pmodel'] = self.config.get(mysection, 'pmodel')
        
        except:
            raise Exception('Error: could not find pmodel in configuration file %s' % self.config_file)

        try:
            self.meparams['instrumentation'] = self.config.get(mysection, 'instrumentation')
        
        except:
            raise Exception('Error: could not find instrumentation in configuration file %s' % self.config_file)

        try:
            self.meparams['exemode'] = self.config.get(mysection, 'exemode')
        
        except:
            raise Exception('Error: could not find exemode in configuration file %s' % self.config_file)

        try:
            self.meparams['batchcmd'] = self.config.get(mysection, 'batchcmd')
        
        except:
            raise Exception('Error: could not find batchcmd in configuration file %s' % self.config_file)


        try:
            self.meparams['jobname'] = self.config.get(mysection, 'jobname')
        
        except:
            raise Exception('Error: could not find jobname in configuration file %s' % self.config_file)

        try:
            self.meparams['walltime'] = self.config.get(mysection, 'walltime')
        
        except:
            raise Exception('Error: could not find walltime in configuration file %s' % self.config_file)

        try:
            self.meparams['maxprocessor'] = self.config.get(mysection, 'maxprocessor')
        
        except:
            raise Exception('Error: could not find maxprocessor in configuration file %s' % self.config_file)

        try:
            self.meparams['accountname'] = self.config.get(mysection, 'accountname')
        
        except:
            raise Exception('Error: could not find accountname in configuration file %s' % self.config_file)

        try:
            self.meparams['buffersize'] = self.config.get(mysection, 'buffersize')
        
        except:
            raise Exception('Error: could not find buffersize in configuration file %s' % self.config_file)

        try:
            self.meparams['msgsize'] = self.config.get(mysection, 'msgsize')
        
        except:
            raise Exception('Error: could not find msgsize in configuration file %s' % self.config_file)

        try:
            self.meparams['stacksize'] = self.config.get(mysection, 'stacksize')
        
        except:
            raise Exception('Error: could not find stacksize in configuration file %s' % self.config_file)


        try:
            self.meparams['counters'] = self.config.get(mysection, 'counters')
        
        except:
            raise Exception('Error: could not find counters in configuration file %s' % self.config_file)

        try:
            self.meparams['commode'] = self.config.get(mysection, 'commode')
        
        except:
            raise Exception('Error: could not find commode in configuration file %s' % self.config_file)


        try:
            self.meparams['memorysize'] = self.config.get(mysection, 'memorysize')
        
        except:
            raise Exception('Error: could not find memorysize in configuration file %s' % self.config_file)


        try:
            self.meparams['queue'] = self.config.get(mysection, 'queue')
        
        except:
            raise Exception('Error: could not find queue in configuration file %s' % self.config_file)

        try:
            self.meparams['input'] = self.config.get(mysection, 'input')

        except:
            raise Exception('Error: could not find input in configuration file %s' % self.config_file)

        try:
            self.meparams['inputdir'] = self.config.get(mysection, 'inputdir')

        except:
            raise Exception('Error: could not find inputdir in configuration file %s' % self.config_file)

        try:
            self.meparams['inputfiles'] = self.config.get(mysection, 'inputfiles')

        except:
            raise Exception('Error: could not find inputfiles in configuration file %s' % self.config_file)








