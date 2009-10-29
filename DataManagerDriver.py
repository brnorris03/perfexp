#!/usr/bin/python

from params import *
from PerfDMFDB import *
from XeonMeasurementEnv import *

def main():
              
    print 'loading data\n'

    Me = XeonMeasurementEnv()
    Me.loadTrials()

    print 'finish loading data\n'

if __name__ == "__main__":

    main()
