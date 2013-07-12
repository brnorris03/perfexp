#!/usr/bin/python

from storage.tools.hpctoolkit import HPCToolkitDB 
from me.platforms.iforge import iForge
from me.params import MEParams
from storage.params import DBParams as Params
  
def main():
              
    print 'loading data\n'

    meParams = MEParams()
    meParams._processConfigFile()

    dbParams = Params()
    dbParams._processConfigFile()		

    mEnv = iForge()
    mEnv.loadTrials(storage = HPCToolkitDB())

    print 'finish loading data\n'

if __name__ == "__main__":

    main()
