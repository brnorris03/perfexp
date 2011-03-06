#!/usr/bin/python
  
from me.platforms.aix import BluePrint
from me.tools.notimer import Collector as NoTimer 
from me.params import MEParams
from storage.params import DBParams 
import os, commands
	
def main():
	
	paramsdir = os.environ.get("PERFEXPDIR") + '/src/examples/params'
	examplesdir = os.environ.get("PERFEXPDIR") + '/src/examples'

	dirList=os.listdir(paramsdir)

	for fname in dirList:
		filename = paramsdir + '/' + fname
		cpcmd = 'cp ' + filename + ' ' + examplesdir + '/params.txt'
		commands.getstatusoutput(cpcmd)  	
		meParams = MEParams()
		meParams._processConfigFile()
	
		dbParams = DBParams()
		dbParams._processConfigFile()

		measurementEnvironment = BluePrint()

		dataCollector = NoTimer()
	
		dataCollector.setCounters()
		perfCmd = dataCollector.getCommand()
		measurementEnvironment.runApp(perfCmd)
	
if __name__ == "__main__":

    main()

