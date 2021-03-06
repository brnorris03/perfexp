#!/usr/bin/python                                                           
import os
from me.interfaces import AbstractCollector
from me.params import MEParams

class Collector(AbstractCollector):

    def setCounters(self):

        f = open('events.xml', 'w')

        print >>f, '<?xml version="1.0" encoding="UTF-8" ?>'

        myCounters = MEParams.meparams['counters'].split()

        if MEParams.meparams['perfmode'] == 'count':
            print >>f, '<ps_hwpc_eventlist class="PAPI">'
            for i in range (0, len(myCounters)):
                print >>f,  '<ps_hwpc_event type="preset" name="' + myCounters[i] + '" />'        
            print >>f, '</ps_hwpc_eventlist>'

        elif MEParams.meparams['perfmode'] == 'profile':
            print >>f, '<ps_hwpc_profile class="PAPI">'
            print >>f, '<ps_hwpc_event type="preset" name="' + myCounters[i] + '"' +' threshold="' + MEParams.meparams['samplingrate'] + '"/>'        
            print >>f, '</ps_hwpc_profile>'

        movecmd = 'mv '+ os.getcwd() + '/' + 'events.xml ' + MEParams.meparams['workdir'] + '/'
        os.popen(movecmd)

        os.environ["PS_HWPC_CONFIG"] = MEParams.meparams['workdir'] + '/events.xml'

	f.close()

    def getCommand(self):

        if MEParams.meparams['instrumentation'] == "runtime":
            if MEParams.meparams['pmodel'] == "omp":
                cmd = 'psrun -p '
            elif MEParams.meparams['pmodel'] == "mpi":
                cmd = 'psrun -f '
            elif MEParams.meparams['pmodel'] == "mpi:omp":
                cmd = 'psrun -f -p '
            else:
                cmd = 'psrun '
        else:
            cmd  = ' '

        return cmd

    def getDataFormat(self):

        return 'psrun'
