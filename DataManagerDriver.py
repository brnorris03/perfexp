#!/usr/bin/python

from params import *
from PerfDMFDB import *
from AIXMeasurementEnv import *

def main():
              
    print 'loading data\n'

    Me = AIXMeasurementEnv()
    Me.loadTrials()

    print 'finish loading data\n'

if __name__ == "__main__":

    main()
