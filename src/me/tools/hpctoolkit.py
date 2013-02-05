#!/usr/bin/python                                                           
import os
from me.interfaces import AbstractCollector
from me.params import MEParams

class Collector(AbstractCollector):

    def __init__(self):
        self.options = ''

    def setCounters(self):
        self.options = ' -e ' + ' -e '.join(MEParams.meparams['counters'].split())


    def getCommand(self):

        if MEParams.meparams['instrumentation'] == "runtime":
            if MEParams.meparams['pmodel'] in ["mpi","mpi:omp"]:
                cmd = MEParams.meparams['mpicmd'] + ' hpcrun '
            else:
                cmd = 'hpcrun '
        else:
            cmd  = ' '

        return cmd

    def getDataFormat(self):

        return 'hpcstruct'
