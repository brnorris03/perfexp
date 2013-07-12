#!/usr/bin/python

from me.tools.hpctoolkit import Collector as HPCCollector
from storage.interfaces import AbstractStorage
import commands, os
from me.params import MEParams
from storage.params import DBParams

class HPCToolkitDB(AbstractStorage):

    def load(self, destdir, trial):

        DataCollector = HPCCollector()
        self.dataFormat = DataCollector.getDataFormat()

        fileList=os.listdir(destdir)

        for ff in fileList:
            if not ff.find('hpctoolkit-'):
                measurementsdir = ff

        loadCommand = 'cd ' + destdir + ' && hpcprof -S ' + MEParams.meparams['exec'] + '.hpcstruct -I ' + MEParams.meparams['srcdir'] + '/\'*\' ' + measurementsdir

        commands.getstatusoutput(loadCommand)
        print 'debug:load command: ', loadCommand

