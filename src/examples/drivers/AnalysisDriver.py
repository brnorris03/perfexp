#!/usr/bin/python


from analysis.tools.tau import PerfExplorer
from analysis.metrics.time import WallClock
from analysis.metrics.memory import L2BW
from analysis.metrics.cpu import MFLIPS

def main():
 
    try: 
        metric = WallClock(params=metricparams)
    except: 
        metric = WallClock(params={})
        
    analysis = PerfExplorer()
    analysis.runAnalysis(metric)

if __name__ == "__main__":

    main()
