#!/usr/bin/python

from me.tools.tau import Collector as TAUCollector
from storage.interfaces import AbstractStorage
import commands, os
from storage.params import DBParams

class PerfDMFDB(AbstractStorage):

    def load(self, destdir, trial):

        DataCollector = TAUCollector()
        self.dataFormat = DataCollector.getDataFormat()

        if self.dataFormat == 'profiles':
            loadCommand = 'java -jar ' + DBParams.dbparams['cqosloaderdir'] + '/' + DBParams.dbparams['cqosloader'] + ' -a ' + DBParams.dbparams['appname'] + ' -e ' + DBParams.dbparams['expname'] + ' -t ' + trial + ' -c ' + DBParams.dbparams['dbconfig']  + ' -d ' + destdir

        elif self.dataFormat == 'psrun':
            loadCommand = 'perfdmf_loadtrial -c ' + DBParams.dbparams['dbconfig'] + ' -a ' + DBParams.dbparams['appname'] + ' -x ' + DBParams.dbparams['expname'] + ' -f ' + self.dataFormat + ' -n ' + trial + ' ' + destdir + '/*.xml'

        checkMetadataFile = ""

        if not os.path.isfile(destdir + '/' + 'metadata.txt'):
            checkMetadataFile = 'touch ' + destdir + '/' + 'metadata.txt'
            commands.getstatusoutput(checkMetadataFile)
            print 'debug:checking for metadata.txt: ', checkMetadataFile

        commands.getstatusoutput(loadCommand)
        print 'debug:load command: ', loadCommand

