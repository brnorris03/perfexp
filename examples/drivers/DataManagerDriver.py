#!/usr/bin/python

from params import *

import util.setup
from storage.tools.tau import PerfDMFDB 
from me.platforms.aix import BluePrint

def main():
              
    util.setup.setPythonPath()     # automatically set the Python search path
    
    print 'loading data\n'

    mEnv = BluePrint()
    mEnv.loadTrials(storage=PerfDMFDB())

    print 'finish loading data\n'

if __name__ == "__main__":

    main()
