#!/usr/bin/python

from params import *
from storage.tools.tau import PerfDMFDB 
from me.platforms.aix import BluePrint

def main():
              
    print 'loading data\n'

    mEnv = BluePrint()
    mEnv.loadTrials(storage = PerfDMFDB())

    print 'finish loading data\n'

if __name__ == "__main__":

    main()
