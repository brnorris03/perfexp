#!/usr/bin/python

from params import *
from me.tools.tau import Collector as TAUCollector
from storage.interfaces import AbstractStorage
import commands, os

class PerfDMFDB(AbstractStorage):

    def load(self, destdir, trial):

        DataCollector = TAUCollector()
        self.dataFormat = DataCollector.getDataFormat()

        if self.dataFormat == 'profiles':
            loadCommand = 'java -jar ' + cqosloaderdir + '/' + cqosloader + ' -a ' + appname + ' -e ' + expname + ' -t ' + trial + ' -c ' + dbconfig  + ' -d ' + destdir

        elif self.dataFormat == 'psrun':
            loadCommand = 'perfdmf_loadtrial -c ' + dbconfig + ' -a ' + appname + ' -x ' + expname + ' -f ' + self.dataFormat + ' -n ' + trial + ' ' + destdir + '/*.xml'

        checkMetadataFile = ""

        if not os.path.isfile(destdir + '/' + 'metadata.txt'):
            checkMetadataFile = 'touch ' + destdir + '/' + 'metadata.txt'
            commands.getstatusoutput(checkMetadataFile)
            print 'debug:checking for metadata.txt: ', checkMetadataFile

        commands.getstatusoutput(loadCommand)
        print 'debug:load command: ', loadCommand

