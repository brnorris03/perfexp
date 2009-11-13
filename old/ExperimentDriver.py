#!/usr/bin/python

from params import *
from AIXMeasurementEnv import *
from TAUCollector import *
import os, commands
	
def main():

    MeasurementEnvironment = AIXMeasurementEnv()
    DataCollector = TAUCollector()

    DataCollector.setCounters()
    perfCmd = DataCollector.getCommand()
    MeasurementEnvironment.runApp(perfCmd)
	
if __name__ == "__main__":

    main()

