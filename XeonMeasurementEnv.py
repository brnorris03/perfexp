#!/usr/bin/python

import os
from params import *

class XeonMeasurementEnv:

    def initialize(self):

        #os.environ["OMP_NUM_THREADS"] = threads
        # TODO: set hardware events 
        if 0:
            print 'DEBUG: OMP_NUM_THREADS=', os.environ.get('OMP_NUM_THREADS')
        

           
        
