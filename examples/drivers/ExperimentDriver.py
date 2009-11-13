#!/usr/bin/python

from params import *

import util.setup 
from me.platforms.aix import BluePrint
from me.tools.tau import Collector as TAUCollector 
import os, commands
	
def main():

	util.setup.setPythonPath()     # automatically set the Python search path
	
	measurementEnvironment = BluePrint()
	dataCollector = TAUCollector()
	
	dataCollector.setCounters()
	perfCmd = dataCollector.getCommand()
	measurementEnvironment.runApp(perfCmd)
	
if __name__ == "__main__":

    main()

