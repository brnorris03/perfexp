#!/usr/bin/python


from analysis.tools.tau import PerfExplorer
from analysis.tools.gups import Hpcc
from analysis.metrics.time import WallClock
from analysis.metrics.memory import L2BW
from analysis.metrics.cpu import MFLIPS
from analysis.params import ANSParams
from storage.params import DBParams 
from me.params import MEParams

def main():

    meParams = MEParams()
    meParams._processConfigFile()

    dbParams = DBParams()
    dbParams._processConfigFile()

    ansParams = ANSParams()
    ansParams._processConfigFile()
 
    try: 
        metric = WallClock(params=ANSParams.ansparams['metricparams'])
    except: 
        metric = WallClock(params={})
        
    analysis = Hpcc()
    analysis.runAnalysis(metric)

if __name__ == "__main__":

    main()
