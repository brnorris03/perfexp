#!/usr/bin/python

from analysis.interfaces import AbstractAnalyzer
from analysis.params import ANSParams
from storage.params import DBParams
from me.params import MEParams

import commands, sys, os

class HPCToolkit(AbstractAnalyzer):

    def runAnalysis(self, metric):

        if MEParams.meparams['pmodel'] == "omp":
            for p in MEParams.meparams['processes'].split():
                for t in MEParams.meparams['threads'].split():
                    destdir = MEParams.dbparams['workdir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-p' + p + 't' + t

        elif MEParams.meparams['pmodel'] == "mpi":
            for p in MEParams.meparams['nodes'].split():
                for t in MEParams.meparams['tasks_per_node'].split():
                    for t2 in MEParams.meparams['threads'].split():
                        for i in MEParams.meparams['input'].split():
                            destdir = MEParams.meparams['workdir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-p' + p + 't' + t + 't2' + t2 + 'i'+i
        
        fileList=os.listdir(destdir)

        fname = 'hpctoolkit-' + MEParams.meparams['exec'] + '-database'

        for ff in fileList:
            if not ff.find(fname):
                databasedir = ff

        if MEParams.meparams['perfmode'] == 'profiling':        
            analyzeCommand = 'hpcviewer ' + destdir + '/' + databasedir
        elif MEParams.meparams['perfmode'] == 'tracing':           
            analyzeCommand = 'hpctraceviewer ' + destdir + '/' + databasedir

        if MEParams.meparams['DEBUG'] == "1":
            print 'debug:analysis command: ', analyzeCommand
        
        commands.getstatusoutput(analyzeCommand)





