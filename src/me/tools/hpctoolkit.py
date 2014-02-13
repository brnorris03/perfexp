#!/usr/bin/python                                                           
import os
from me.interfaces import AbstractCollector
from me.params import MEParams

class Collector(AbstractCollector):

    def __init__(self):
        self.options = ''

    def setCounters(self):

        counters = MEParams.meparams['counters'].split()

        for i in range(0,len(counters)):
            self.options += ' -e ' + counters[i] + '@' + MEParams.meparams['samplingrate'] + ' '    
        return self.options    

    def getCommand(self):

        cmd = ' '

        if MEParams.meparams['instrumentation'] == "runtime":
            if MEParams.meparams['perfmode'] == "tracing":
                cmd = 'hpcrun -t'
            elif MEParams.meparams['perfmode'] == "profiling":
                cmd = 'hpcrun '

        return cmd

    def getDataFormat(self):

        return 'hpcstruct'
