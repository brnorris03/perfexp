#!/usr/bin/python

from params import *
from analysis.metrics.time import WallClock
from analysis.interfaces import AbstractAnalyzer
from vis.tools.pylab import Plotter
import commands, sys, os

class Gprof(AbstractAnalyzer):

    def runAnalysis(self, metric):

        ydata = []

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
            for n in processes:
                P = n
                xdata.append(P)

        plotter.genPlot(xdata, ydata)

        cmd = 'chmod u+x ' + plotfilename 
        commands.getstatusoutput(cmd)
        moveResultsCommand = 'mv ' + os.getcwd() + '/'+ plotfilename + ' ' + resultsdir
        commands.getstatusoutput(moveResultsCommand)




