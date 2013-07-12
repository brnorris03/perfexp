#!/usr/bin/python

from me.tools.tau import Collector as TAUCollector
from storage.interfaces import AbstractStorage
import commands, os
from me.params import MEParams

class Gprof(AbstractStorage):

    def load(self, destdir, trial):

        convertcmd = 'gprof ' + MEParams.meparams['cmdline'] + ' ' + destdir + '/gmon.out >& ' + destdir + '/gprof.out'
        if MEParams.meparams['DEBUG'] == "1":
            print convertcmd
        commands.getstatusoutput(convertcmd)
