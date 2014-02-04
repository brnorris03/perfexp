#!/usr/bin/python

# -------
# imports
# -------

from storage.tools.hpctoolkit import HPCToolkitDB 
from me.platforms.iforge import iForge
from me.params import MEParams
from storage.params import DBParams as Params


# ----
# main
# ----
  
def main():
    
    # Should this go in an if(debug) block?          
    print 'loading data\n'

    # Get ExperimentDriver values from params file
    meParams = MEParams()
    meParams._processConfigFile()
    # Get DataManager values from params file
    dbParams = Params()
    dbParams._processConfigFile()		
    # Create measuring environment, and load trials <<< this should be modular
    mEnv = iForge()
    mEnv.loadTrials(storage = HPCToolkitDB())
    
    # Should this go in an if(debug) block?
    print 'finish loading data\n'

if __name__ == "__main__":

    main()
