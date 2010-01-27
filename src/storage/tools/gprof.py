#!/usr/bin/python

from params import *
from me.tools.tau import Collector as TAUCollector
from storage.interfaces import AbstractStorage
import commands, os

class Gprof(AbstractStorage):

    def load(self, destdir, trial, process, thread):

        convertcmd = 'gprof ' + cmdline + ' ' + destdir + '/gmon.out >& ' + destdir + '/gprof.out'
        if DEBUG == 1:
            print convertcmd
        commands.getstatusoutput(convertcmd)
