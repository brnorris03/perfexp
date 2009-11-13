#!/usr/bin/python

from params import *
import commands

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
        cmd = 'chmod u+x plot.py'
        commands.getstatusoutput(cmd)

    def writeGeneratePlot(self, f):

        print >>f, 'def generatePlot(xdata,ydata):'

        print >>f, '\tf=open(\'plot.py\',\'a\')'

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

