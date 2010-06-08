#!/usr/bin/python
  
from me.platforms.aix import BluePrint
from me.tools.tau import Collector as TAUCollector 
from me.tools.notimer import Collector as NoTimer 
from me.params import MEParams
from storage.params import DBParams 
import os, commands
	
def main():
	
	meParams = MEParams()
	meParams._processConfigFile()
	
	dbParams = DBParams()
	dbParams._processConfigFile()

	measurementEnvironment = BluePrint()

	dataCollector = NoTimer()
	
	dataCollector.setCounters()
	print 'set counters'
	perfCmd = dataCollector.getCommand()
	print perfCmd
	measurementEnvironment.runApp(perfCmd)
	print 'run app'
	
if __name__ == "__main__":

    main()

