#!/usr/bin/python

# -------
# imports
# -------

from me.platforms.iforge import iForge
from me.params import MEParams
from storage.params import DBParams 
from common.globals import Globals
import os, commands


# ----
# main
# ----

def main():
	# Get params and examples directories	
	paramsdir = os.environ.get("PERFEXPDIR") + '/src/examples/params'
	examplesdir = os.environ.get("PERFEXPDIR") + '/src/examples'

	# Save contents of params directory
	dirList=os.listdir(paramsdir)

	# Print path to tau directory <<< should this be in a debug block?
	globalParams = Globals()
	globalParams._processConfigFile()
	print globalParams.configparams['taudir']

	# Iterate through all 'params' files 
	for fname in dirList:
		if not fname.startswith('.'):
			# Copy params.txt file to src/examples/
			filename = paramsdir + '/' + fname
			cpcmd = 'cp ' + filename + ' ' + examplesdir + '/params.txt'
			commands.getstatusoutput(cpcmd)
			# Read the 'ExperimentDriver' section of the params file
			meParams = MEParams()
			meParams._processConfigFile()
			# Read the 'DataManager' section of the params file
			dbParams = DBParams()
			dbParams._processConfigFile()
			# Create and run measurement environment <<< This should be modular
			measurementEnvironment = iForge()
			measurementEnvironment.runApp()
	
if __name__ == "__main__":

    main()

