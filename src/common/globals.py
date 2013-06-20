# This file is part of PerfExp
# Original author: Boyana Norris, brnorris03@gmail.com
# (c) 2010-2013 UChicago Argonne, LLC
# For copying information, see the file LICENSE

import logging, os

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
        pass
