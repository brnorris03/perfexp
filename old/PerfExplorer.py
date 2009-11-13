#!/usr/bin/python

from params import *
from WallClock import *
import commands, sys, os

class PerfExplorer:

    def runAnalysis(self):

        f = open('analysis.py', 'w')
        self.genAnalysisScript(f)
        f.close()

        analyzeCommand = 'perfexplorer -n -c '
        analyzeCommand += dbconfig + ' -i ' + os.getcwd() + '/analysis.py'
        moveResultsCommand = 'mv ' + os.getcwd() + '/plot.py ' + resultsdir
        moveResultsCommand2 = 'mv ' + os.getcwd() + '/analysis.py ' + resultsdir

        print 'debug:analysis command: ', analyzeCommand
        print 'debug: move results command: ', moveResultsCommand
        
        commands.getstatusoutput(analyzeCommand)
        commands.getstatusoutput(moveResultsCommand)
        commands.getstatusoutput(moveResultsCommand2)

    def genAnalysisScript(self, f):
        self.writeHeader(f)
        self.writeGetParameters(f)
        self.writeLoadExperiments(f)
        self.writeDeriveMetric(f)
        self.writeSortedDictValues(f)
        self.writeGeneratePlot(f)
        cm = WallClock()
        cm.writeMetricMethod(f)
        self.writeMain(f)

    def writeHeader(self, f):

        print >>f, '#!/usr/bin/env python'
        print >>f, 'from edu.uoregon.tau.perfexplorer.glue import *'
        print >>f, 'from edu.uoregon.tau.perfdmf import Trial'
        print >>f, 'from edu.uoregon.tau.perfexplorer.client import PerfExplorerModel'
        print >>f, 'from edu.uoregon.tau.perfexplorer.rules import *'
        print >>f, 'from java.util import HashSet'
        print >>f, 'from java.util import ArrayList'
        print >>f, 'from java.util.regex import Pattern'
        print >>f, 'from java.util.regex import Matcher'

        print >>f, 'True = 1'
        print >>f, 'False = 0\n'

    def writeGetParameters(self, f):

        print >>f, 'def getParameters():'
        print >>f, '\tglobal parameterMap'
        print >>f, '\tglobal config'
        print >>f, '\tglobal fileName'
        print >>f, '\tprint "getting parameters..."'
        print >>f, '\tparameterMap = PerfExplorerModel.getModel().getScriptParameters()'
        print >>f, '\tkeys = parameterMap.keySet()'
        print >>f, '\tfor key in keys:'
        print >>f,    '\t\tprint key, parameterMap.get(key)'
        print >>f, '\tconfig = parameterMap.get("config")'

        print >>f, '\tfileName = parameterMap.get("fileName")'
        print >>f, '\tprint "...done."\n'

    def writeLoadExperiments(self, f):

        print >>f, 'def loadExperiments(app=\'default\'):'
        print >>f, '\tprint "loading data..."'
        print >>f, '\tUtilities.setSession(config)'
        print >>f, '\texperiments = Utilities.getExperimentsForApplication(app)'
        print >>f, '\tprint "...done."'
        print >>f, '\treturn experiments\n'

    def writeDeriveMetric(self, f):

        print >>f, 'def deriveMetric(input, first, second, oper):'
        print >>f, '\t# derive the metric'
        print >>f, '\tderivor = DeriveMetricOperation(input, first, second, oper)'
        print >>f, '\tderived = derivor.processData().get(0)'
        print >>f, '\tnewName = derived.getMetrics().toArray()[0]'
        print >>f, '\t# merge new metric with the trial'

        print >>f, '\tmerger = MergeTrialsOperation(input)'
        print >>f, '\tmerger.addInput(derived)'
        print >>f, '\tmerged = merger.processData().get(0)'
        print >>f, '\t#print "new metric: " + newName'

        print >>f, '\treturn merged, newName\n'

    def writeSortedDictValues(self, f):

        print >>f, 'def sortedDictValues(adict):'
        print >>f, '\tkeys = adict.keys()'
        print >>f, '\tkeys.sort()'
        print >>f, '\treturn map(adict.get, keys), keys\n'

    def writeGeneratePlot(self, f):

        print >>f, 'def generatePlot(data):'

        print >>f, '\tsortedValues, sortedKeys = sortedDictValues(data)'
        print >>f, '\tf=open(\'plot.py\',\'a\')'

        print >>f, '\tprint >>f, \'#!/usr/bin/env python\''
        print >>f, '\tprint >>f, \'\\nfrom pylab import *\''

        print >>f, '\txstring = \'\\nt = [\''

        print >>f, '\tfor procs in sortedKeys:'
        print >>f, '\t\txstring += str(procs) +\',\''

        print >>f, '\txstring += \']\''
        print >>f, '\tprint >>f, xstring'
        print >>f, '\tystring = \'\\ns = [\''

        print >>f, '\tfor d in sortedValues:'
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


    def writeMain(self, f):

        print >>f, 'if __name__ == "__main__":'
        print >>f, '\tglue()'


