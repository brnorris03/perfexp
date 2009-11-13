#!/usr/bin/python                                                           
from params import *
import os
from perfexp.me.collector import AbstractCollector

class Collector(AbstractCollector):

    def setCounters(self):

        f = open('events.xml', 'w')

        print >>f, '<?xml version="1.0" encoding="UTF-8" ?>'
        print >>f, '<ps_hwpc_eventlist class="PAPI">'

        for i in range (0, len(counters)):
            print >>f,  '<ps_hwpc_event type="preset" name="' + counters[i] + '" />'

        print >>f, '</ps_hwpc_eventlist>'

        os.environ["PS_HWPC_CONFIG"] = os.getcwd() + '/' + 'events.xml'
	f.close()

    def getCommand(self):

        if instrumentation == 'runtime':
            if pmodel == 'omp':
                cmd = 'psrun -p '
            elif pmodel == 'mpi':
                cmd = 'psrun -f '
            elif pmodel == 'mpi:omp':
                cmd = 'psrun -f -p '
            else:
                cmd = 'psrun '
        else:
            cmd  = ' '

        return cmd

    def getDataFormat(self):

        return 'psrun'
