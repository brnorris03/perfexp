# This file is part of PerfExp
# Original author: Boyana Norris, brnorris03@gmail.com
# (c) 2010-2013 UChicago Argonne, LLC
# For copying information, see the file LICENSE

import logging, os
import ConfigParser

# Global singleton class for various runtime options 
def Globals():
    '''Helper function to ensure exactly one instance of the Globals_singleton class exists'''
    myglobals = None
    try:
        myglobals = Globals_Singleton()
    except Globals_Singleton, s:
        myglobals = s
    return myglobals

class Globals_Singleton:
    '''A singleton class in which to stash various useful global variables for bocca.
    Do not instantiate this class directly, rather use the Globals helper function,
    e.g., myglobals = Globals().
    '''
    __single = None  # Used for ensuring singleton instance
    def __init__(self):
        if Globals_Singleton.__single:
            raise Globals_Singleton.__single 
        Globals_Singleton.__single = self

        self.dry_run = False     # When True, don't execute anything, just print commands
        
        self.shell = '/bin/sh'   # Shell used by contractor 
        
        # Configure logging
        self.logger = logging.getLogger("PerfExp")
        self.logfile = 'perfexp.log'
        self.logger.addHandler(logging.FileHandler(filename=self.logfile))
        # Because commands are output with extra formatting, for now do not use the logger for stderr output
        #streamhandler = logging.StreamHandler()
        #streamhandler.setLevel(logging.INFO)
        #self.logger.addHandler(streamhandler)
        
        # Formatting (e.g., color) settings
        self.error_pre = "\x1B[00;31m"
        self.error_post = "\x1B[00m"

        # Enable debugging
        if 'PERFEXP_DEBUG' in os.environ.keys() and os.environ['PERFEXP_DEBUG'] == '1': 
            self.debug = True
            self.logger.setLevel(logging.DEBUG)
        else: 
            self.debug = False
            self.logger.setLevel(logging.INFO)
#        pass

        # initialize configuration file parameters
        self.configparams = {'lmbenchdir':None, 'blackjackdir':None, 'skampidir':None, 'papidir':None,'taudir':None,'hpctoolkitdir':None,'perfsuitedir':None}
        self.config = ConfigParser.ConfigParser()
        self.config_file = os.environ.get("PERFEXPDIR") + '/src/config/config.txt'
        
    def _processConfigFile(self):
        
        benchmarksection = 'Benchmarks'
        toolssection = 'Tools'

        self.config.readfp(open(self.config_file))

        try:
            newparam = 'lmbenchdir'
            self.configparams[newparam] = self.config.get(benchmarksection, newparam)
        except:
            raise Exception('Error: could not find lmbenchdir in configuration file %s' % self.config_file)


        try:
            newparam = 'blackjackdir'
            self.configparams[newparam] = self.config.get(benchmarksection, newparam)
        except:
            raise Exception('Error: could not find blackjackdir in configuration file %s' % self.config_file)

        try:
            newparam = 'skampidir'
            self.configparams[newparam] = self.config.get(benchmarksection, newparam)
        except:
            raise Exception('Error: could not find skampidir in configuration file %s' % self.config_file)


        try:
            newparam = 'papidir'
            self.configparams[newparam] = self.config.get(toolssection, newparam)
        except:
            raise Exception('Error: could not find papidir in configuration file %s' % self.config_file)

        try:
            newparam = 'taudir'
            self.configparams[newparam] = self.config.get(toolssection, newparam)
        except:
            raise Exception('Error: could not find taudir in configuration file %s' % self.config_file)

        try:
            newparam = 'hpctoolkitdir'
            self.configparams[newparam] = self.config.get(toolssection, newparam)
        except:
            raise Exception('Error: could not find hpctoolkitdir in configuration file %s' % self.config_file)

        try:
            newparam = 'perfsuitedir'
            self.configparams[newparam] = self.config.get(toolssection, newparam)
        except:
            raise Exception('Error: could not find perfsuitedir in configuration file %s' % self.config_file)




