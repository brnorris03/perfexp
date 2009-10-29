#!/usr/bin/python

from params import *
from XeonMeasurementEnv import *
from TAUCollector import *
import os, commands
	
def main():

    MeasurementEnvironment = XeonMeasurementEnv()
    DataCollector = TAUCollector()

    DataCollector.setCounters()
    perfCmd = DataCollector.getCommand()
    MeasurementEnvironment.runApp(perfCmd)
	
if __name__ == "__main__":

    main()

