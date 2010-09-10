#!/usr/bin/python
  
from me.platforms.aix import BluePrint
from me.platforms.cobalt import Cobalt
from me.platforms.xeon import Generic
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

	measurementEnvironment = Generic()

	dataCollector = TAUCollector()
	
	dataCollector.setCounters()
	perfCmd = dataCollector.getCommand()
	measurementEnvironment.runApp(perfCmd)
	
if __name__ == "__main__":

    main()

