#!/usr/bin/python

# -------
# imports
# -------

from analysis.tools.hpctoolkit import HPCToolkit
from analysis.metrics.time import WallClock
from analysis.params import ANSParams
from storage.params import DBParams 
from me.params import MEParams


# ----
# main
# ----

def main():
    # Get 'ExperimentDriver' values from params file
    meParams = MEParams()
    meParams._processConfigFile()
    # Get 'DataManager' values from params file
    dbParams = DBParams()
    dbParams._processConfigFile()
    # Get 'Analysis' values from params file
    ansParams = ANSParams()
    ansParams._processConfigFile()
    # needs comment
    try: 
        metric = WallClock(params=ANSParams.ansparams['metricparams'])
    except: 
        metric = WallClock(params={})
    # Create analysis tool and launch  
    analysis = HPCToolkit()
    analysis.runAnalysis(metric)

if __name__ == "__main__":
    main()
