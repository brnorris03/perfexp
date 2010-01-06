#!/usr/bin/python

from params import *
import os
from me.interfaces import AbstractCollector

class Collector(AbstractCollector):

    def setCounters(self):
       pass
			
    def getCommand(self):

        mycommand = ''
        
        return mycommand

    def getDataFormat(self):
        
        return 'gprof'
