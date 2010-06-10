#!/usr/bin/python

from analysis.metrics.time import WallClock
from analysis.interfaces import AbstractAnalyzer
from vis.tools.pylab import Plotter
import commands, sys, os, dircache
from analysis.params import ANSParams
from storage.params import DBParams
from me.params import MEParams

class Ltimer(AbstractAnalyzer):

    def runAnalysis(self, metric):

        ydata = []
	
	if MEParams.meparams['pmodel'] == "omp":
	    
	    for p in  MEParams.meparams['nodes'].split():
                for t in MEParams.meparams['threads'].split():
                    dirname = DBParams.dbparams['datadir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-' + 'p' + p +'t' + t 
		    files = dircache.listdir(dirname)
                    for ff in files:
        		if ff.find('.err'):
                		break

                    filename = DBParams.dbparams['datadir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-' + 'p' + p +'t' + t + '/' + ff
                    f = file(filename)
                    lines = f.read().split('\n')

                    lines[1] = lines[1].replace('Real','')
                    lines[1] = lines[1].replace(' ','')
                    ydata.append(str(float(lines[1])))


	else:
            for p in MEParams.meparams['processes'].split():
                for t in MEParams.meparams['threads'].split():
                    filename = DBParams.dbparams['datadir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-' + 'p' + p +'t' + t + '/' + 'ltimer.out'
                    f = file(filename)
                    line =f.readline()
                    words = line.rsplit()
                    words[0] = words[0].replace('user','')
                    ydata.append(str(float(words[0])))

        self.writeGeneratePlot(ydata)
                 
    def writeGeneratePlot(self, ydata):

        xdata = []
        plotter = Plotter()

        if MEParams.meparams['pmodel'] == "mpi":
	    if MEParams.meparams['nodes']:
                for n in MEParams.meparams['nodes'].split():
                    P = n
                    xdata.append(P)

            else:	
                for n in MEParams.meparams['processes'].split():
                    P = n
                    xdata.append(P)
        elif MEParams.meparams['pmodel'] == "omp":
            for n in MEParams.meparams['threads'].split():
                T=n
                xdata.append(T)

        plotter.genPlot(xdata, ydata)

        cmd = 'chmod u+x ' + ANSParams.ansparams['plotfilename'] 
        commands.getstatusoutput(cmd)
        moveResultsCommand = 'mv ' + os.getcwd() + '/'+ ANSParams.ansparams['plotfilename'] + ' ' + ANSParams.ansparams['resultsdir']
        commands.getstatusoutput(moveResultsCommand)




