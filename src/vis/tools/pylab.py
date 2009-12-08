#!/usr/bin/python

from params import *
import commands,os

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
        moveResultsCommand = 'mv ' + os.getcwd() + '/model.py ' + resultsdir
        moveResultsCommand2 = 'mv ' + os.getcwd() + '/model-plot.py ' + resultsdir
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
        
        filename = resultsdir + '/plot.py' 
        infile = open(filename,"r")
        text = infile.read()
        infile.close()
        search = "s = "
        index = text.find(search)
        index2 = text.find("\n", index)
        data3 = text[index:index2]

        print >>f, data3
        print >>f, 'fig = plt.figure()'
        print >>f, 'ax = fig.add_subplot(111)'
        print >>f, 'p1, = ax.plot(t, s, \'k--\')'
        print >>f, 'p2, =  ax.plot(t, r,\'k:\')'

        print >>f, 'ax.set_xlabel("', xaxislabel, '")'

        print >>f, 'ax.set_ylabel("', yaxislabel, '")'

        print >>f, 'ax.set_title("', graphtitle,'")'

        print >>f, 'ax.legend((p1,p2),("', legend[0],'", "', legend[1],'"))'

        print >>f, 'ax.grid(True)'
        print >>f, 'plt.show()'

        f.close()

        cmd = 'chmod u+x merged-plot.py'
        commands.getstatusoutput(cmd)
        moveResultsCommand = 'mv ' + os.getcwd() + '/merged-plot.py ' + resultsdir
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
        print >>f, '\tprint >>f, \'\\nplot(t, s, linewidth=1.0)\''

        #parameter: x-axis label                                         

        print >>f, '\tprint >>f, \'\\nxlabel("', xaxislabel, '")\''

        #parameter: y-axis label                                       

        print >>f, '\tprint >>f, \'\\nylabel("', yaxislabel, '")\''

        #parameter: graph title                                          

        print >>f, '\tprint >>f, \'\\ntitle("', graphtitle,'")\''

        print >>f, '\tprint >>f, \'\\ngrid(True)\''
        print >>f, '\tprint >>f, \'\\nshow()\''

        print >>f, '\tf.close()\n'

