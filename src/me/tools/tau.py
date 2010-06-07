#!/usr/bin/python

import os
from me.interfaces import AbstractCollector

class Collector(AbstractCollector):

    def setCounters(self):

	for i in range (1, (len(counters) + 1)):	
		os.environ['COUNTER' + str(i)] = counters[i-1]
		if DEBUG==1:
			print 'COUNTER' + str(i) + ': ' + os.environ.get('COUNTER' + str(i))
			
    def getCommand(self):

        if pmodel == 'mpi' and instrumentation == 'runtime':
            mycommand = 'tauex '

            for e in counters:
                mycommand +=  ' -e ' + e + ' '
        else:
		mycommand = ' '

	if DEBUG==1:
        	print 'DEBUG: performance tool command:  ', mycommand
        
        return mycommand

    def getDataFormat(self):
        
        return 'profiles'
