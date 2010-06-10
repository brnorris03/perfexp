#!/usr/bin/python

from analysis.metrics.time import WallClock
from analysis.interfaces import AbstractAnalyzer
from vis.tools.pylab import Plotter
import commands, sys, os
from analysis.params import ANSParams
from storage.params import DBParams
from me.params import MEParams

class Gprof(AbstractAnalyzer):

    def runAnalysis(self, metric):

        ydata = []

	if MEParams.meparams['nodes'] and MEParams.meparams['tasks_per_node']:
	    for p in MEParams.meparams['nodes'].split():
                for t in MEParams.meparams['tasks_per_node'].split():
                    filename = DBParams.dbparams['datadir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-' + 'p' + p +'t' + t + '/' + 'gprof.out'
                    f = file(filename)
                    for line in f:
                        if 'sample hit' in line:
                            break
                    words = line.split()
   	            i = words.index('seconds')
		    avgtime = float(words[i-1]) / int(p)	
                    ydata.append(str(avgtime))

	else:
            for p in MEParams.meparams['processes'].split():
                for t in MEParams.meparams['threads'].split():
                    filename = DBParams.dbparams['datadir'] + '/' + DBParams.dbparams['appname'] + '-' + DBParams.dbparams['expname'] + '-' + DBParams.dbparams['trialname'] + '-' + 'p' + p +'t' + t + '/' + 'gprof.out'
                    f = file(filename)
                    for line in f:
                        if 'sample hit' in line:
                            break
                    words = line.split()
                    i = words.index('seconds')
                    ydata.append(str(float(words[i-1])))

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
            for n in MEParams.meparams['threads']:
                T=n
                xdata.append(T)

        plotter.genPlot(xdata, ydata)

        cmd = 'chmod u+x ' + ANSParams.ansparams['plotfilename'] 
        commands.getstatusoutput(cmd)
        moveResultsCommand = 'mv ' + os.getcwd() + '/'+ ANSParams.ansparams['plotfilename'] + ' ' + ANSParams.ansparams['resultsdir']
        commands.getstatusoutput(moveResultsCommand)




