#!/usr/bin/python

from storage.tools.tau import PerfDMFDB 
from me.platforms.aix import BluePrint
from storage.params import DBParams as Params
  
def main():
              
    print 'loading data\n'

    myParams = Params()
    myParams._processConfigFile		

    mEnv = BluePrint()
    mEnv.loadTrials(storage = PerfDMFDB())

    print 'finish loading data\n'

if __name__ == "__main__":

    main()
