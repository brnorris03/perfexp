#!/usr/bin/python

import os
from me.interfaces import AbstractCollector
from me.params import MEParams

class Collector(AbstractCollector):

    def setCounters(self):
	myCounters = MEParams.meparams['counters'].split()
	for i in range (1, (len(myCounters) + 1)):	
		os.environ['COUNTER' + str(i)] = myCounters[i-1]
		if MEParams.meparams['DEBUG']=="1":
			print 'COUNTER' + str(i) + ': ' + os.environ.get('COUNTER' + str(i))
			
    def getCommand(self):

        if MEParams.meparams['pmodel'] == "mpi" and MEParams.meparams['instrumentation'] == "runtime":
            mycommand = 'tauex '

            for e in myCounters:
                mycommand +=  ' -e ' + e + ' '
        else:
		mycommand = ' '

	if MEParams.meparams['DEBUG']=="1":
        	print 'DEBUG: performance tool command:  ', mycommand
        
        return mycommand

    def getDataFormat(self):
        
        return 'profiles'
