#!/usr/bin/python

from params import *
from analysis.metrics.time import WallClock
from analysis.interfaces import AbstractAnalyzer
from vis.tools.pylab import Plotter
import commands, sys, os

class Gprof(AbstractAnalyzer):

    def runAnalysis(self, metric):

        ydata = []

	if nodes and tasks_per_node:
	    for p,o in map(None, nodes, cmdlineopts):
                for t in tasks_per_node:
                    filename = datadir + '/' + appname + '-' + expname + '-' + trialname + '-' + 'p' + p +'t' + t + '/' + 'gprof.out'
                    f = file(filename)
                    for line in f:
                        if programevent in line:
                            break
                    words = line.split()
   	            i = words.index(programevent)
		    avgtime = float(words[i+1]) / int(p)	
                    ydata.append(str(avgtime))

	else:
            for p,o in map(None, processes, cmdlineopts):
                for t in threads:
                    filename = datadir + '/' + appname + '-' + expname + '-' + trialname + '-' + 'p' + p +'t' + t + '/' + 'gprof.out'
                    f = file(filename)
                    for line in f:
                        if programevent in line:
                            break
                    words = line.split()
                    print words[1]
                    ydata.append(words[1])

        self.writeGeneratePlot(ydata)
                 
    def writeGeneratePlot(self, ydata):

        xdata = []
        plotter = Plotter()

        if pmodel == 'mpi':
	    if nodes:
                for n in nodes:
                    P = n
                    xdata.append(P)

            else:	
                for n in processes:
                    P = n
                    xdata.append(P)

        plotter.genPlot(xdata, ydata)

        cmd = 'chmod u+x ' + plotfilename 
        commands.getstatusoutput(cmd)
        moveResultsCommand = 'mv ' + os.getcwd() + '/'+ plotfilename + ' ' + resultsdir
        commands.getstatusoutput(moveResultsCommand)




