#!/usr/bin/python

import commands,os
from numpy import mean, std, array
from scipy import sqrt
from analysis.params import ANSParams
from examples.models.params import GENParams

from vis.interfaces import AbstractPlotter

class Plotter(AbstractPlotter):

    def generatePlot(self, xdata, ydata):

        f = open('model.py','w')

        print >>f, '#!/usr/bin/env python'

        self.writeGeneratePlot(f)

        print >>f, 'if __name__ == "__main__":'

        print >>f, '\txdata = []'
        print >>f, '\tydata = []'

        for x in xdata:
            print >>f, '\txdata.append(' + str(x) + ')'

        for y in ydata:
            print >>f, '\tydata.append(' + str(y) + ')'

        print >>f, '\tgeneratePlot(xdata,ydata)'

        f.close()

        cmd = 'chmod u+x model.py'
        commands.getstatusoutput(cmd)
        cmd = './model.py'
        commands.getstatusoutput(cmd)
        cmd = 'chmod u+x model-plot.py'
        commands.getstatusoutput(cmd)
        moveResultsCommand = 'mv ' + os.getcwd() + '/model.py ' + ANSParams.ansparams['resultsdir']
        moveResultsCommand2 = 'mv ' + os.getcwd() + '/model-plot.py ' + ANSParams.ansparams['resultsdir']
        commands.getstatusoutput(moveResultsCommand)
        commands.getstatusoutput(moveResultsCommand2)

    def generateMergedPlot(self, xdata, ydata):
        
        f = open('merged-plot.py','w')
        print >>f, '#!/usr/bin/env python'
        print >>f, 'from pylab import *'
        print >>f, 'import matplotlib.pyplot as plt'

        data1 = 't = ['

        for x in xdata:
            data1 += str(x) + ','

        data1 += ']'
        data2 = 'r = ['

        for y in ydata:
            data2 += str(y) + ','

        data2 += ']'

        print >>f, data1
        print >>f, data2
        
        filename = ANSParams.ansparams['resultsdir'] + '/plot.py' 
        infile = open(filename,"r")
        text = infile.read()
        infile.close()
        search = "s = "
        index = text.find(search)
        index2 = text.find("\n", index)
        data3 = text[index:index2]

        index3 = text.find("[", index)
        index4 = text.find(",]", index)

        data4 = text[index3+1:index4]

        print data4

        measured = data4.split(',')
        measuredY = []
        
        for y in measured:
            measuredY.append(float(y))

        if ANSParams.ansparams['DEBUG']: 
            self.computeError(measuredY, ydata)

        print >>f, data3
        print >>f, 'fig = plt.figure()'
        print >>f, 'ax = fig.add_subplot(111)'
        print >>f, 'p1, = ax.loglog(t, s, \'k--\', basex=2, basey=2)'
        print >>f, 'p2, =  ax.loglog(t, r,\'k:\', basex=2, basey=2)'

        print >>f, 'ax.set_xlabel("', ANSParams.ansparams['xaxislabel'], '")'

        print >>f, 'ax.set_ylabel("', ANSParams.ansparams['yaxislabel'], '")'

        print >>f, 'ax.set_title("', ANSParams.ansparams['graphtitle'],'")'
        
        legend = GENParams.modparams['legend'].split()

        print >>f, 'ax.legend((p1,p2),("', legend[0],'", "', legend[1],'"))'

        print >>f, 'ax.grid(True)'
        print >>f, 'plt.show()'

        f.close()

        cmd = 'chmod u+x merged-plot.py'
        commands.getstatusoutput(cmd)
        moveResultsCommand = 'mv ' + os.getcwd() + '/merged-plot.py ' + ANSParams.ansparams['resultsdir']
        commands.getstatusoutput(moveResultsCommand)

    def writeGeneratePlot(self, f):

        print >>f, 'def generatePlot(xdata,ydata):'

        print >>f, '\tf=open(\'model-plot.py\',\'a\')'

        print >>f, '\tprint >>f, \'#!/usr/bin/env python\''
        print >>f, '\tprint >>f, \'\\nfrom pylab import *\''

        print >>f, '\txstring = \'\\nt = [\''

        print >>f, '\tfor procs in xdata:'
        print >>f, '\t\txstring += str(procs) +\',\''

        print >>f, '\txstring += \']\''
        print >>f, '\tprint >>f, xstring'
        print >>f, '\tystring = \'\\ns = [\''

        print >>f, '\tfor d in ydata:'
        print >>f, '\t\tystring += str(d) + \',\''
        print >>f, '\tystring += \']\''
        print >>f, '\tprint >>f, ystring'
        print >>f, '\tprint >>f, \'\\nloglog(t, s, linewidth=1.0,basex=2, basey=2)\''

        #parameter: x-axis label                                         

        print >>f, '\tprint >>f, \'\\nxlabel("', ANSParams.ansparams['xaxislabel'], '")\''

        #parameter: y-axis label                                       

        print >>f, '\tprint >>f, \'\\nylabel("', ANSParams.ansparams['yaxislabel'], '")\''

        #parameter: graph title                                          

        print >>f, '\tprint >>f, \'\\ntitle("', ANSParams.ansparams['graphtitle'],'")\''

        print >>f, '\tprint >>f, \'\\ngrid(True)\''
        print >>f, '\tprint >>f, \'\\nshow()\''

        print >>f, '\tf.close()\n'

    def genPlot(self, xdata, ydata):
        f=open(ANSParams.ansparams['plotfilename'],'a')
        print >>f, '#!/usr/bin/env python'
        print >>f, '\nfrom pylab import *'
        xstring = '\nt = ['
        for procs in xdata:
            xstring += str(procs) +','
        xstring += ']'
        print >>f, xstring
        ystring = '\ns = ['
        for d in ydata:
            ystring += str(d) + ','
        ystring += ']'
        print >>f, ystring
        print >>f, '\nloglog(t, s, linewidth=1.0,basex=2,basey=2)'
        print >>f, '\nxlabel(" ' + ANSParams.ansparams['xaxislabel'] +' ")'
        print >>f, '\nylabel(" ' + ANSParams.ansparams['yaxislabel'] + ' ")'
        print >>f, '\ntitle(" ' + ANSParams.ansparams['graphtitle'] + ' ")'
        print >>f, '\ngrid(True)'
        print >>f, '\nshow()'
        f.close()

    def computeError(self, measured, modeled):

        measured = array(measured)
        modeled = array(modeled)
        n = len(measured)

        print measured
        print 'modeled data: ', modeled
        # calculate residuals (observed - predicted)                              
        mserr = sum((modeled-measured)**2) / n   # Total Sum of Squares                    
        sterr = sqrt(mserr)
    
        # compute the mean square error (variance) and standard error (root of var), R2 and R                                                                  
        print 'Mean square error: ', mserr
        print 'Standard error: ', sterr
