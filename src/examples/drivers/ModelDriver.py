#!/usr/bin/python

# -------
# imports
# -------

from me.platforms.xeon import Generic as XeonMeasurementEnv
from me.platforms.aix import BluePrint as AIXMeasurementEnv
from examples.models.logp_FT import FT
from examples.models.rarma import RARMA
from vis.tools.pylab import Plotter
from examples.models.params import RARMAParams
from analysis.params import ANSParams
from me.params import MEParams
from examples.models.params import GENParams
import os, commands


# ----
# main
# ----
def main():
    # Get params and examples directories
    paramsdir = os.environ.get("PERFEXPDIR") + '/src/examples/params'
    examplesdir = os.environ.get("PERFEXPDIR") + '/src/examples'
    
    # Save contents of params directory
    dirList=os.listdir(paramsdir)
    # Iterate through all 'params' files
    for fname in dirList:
        if not fname.startswith('.'):
            # Copy params.txt file to src/examples/
            filename = paramsdir + '/' + fname
            cpcmd = 'cp ' + filename + ' ' + examplesdir + '/params.txt'
            commands.getstatusoutput(cpcmd)
            # Get values from params file
            modParams = RARMAParams()
            modParams._processConfigFile()
            ansParams = ANSParams()
            ansParams._processConfigFile()
            meParams = MEParams()
            meParams._processConfigFile()
            genParams = GENParams()
            genParams._processConfigFile()
            # comment needed
            vm = AIXMeasurementEnv()
            plotter = Plotter()
            model = RARMA()
            xdata,ydata = vm.validateModel(model)
            plotter.generatePlot(xdata,ydata)
#           plotter.generateMergedPlot(xdata,ydata)

if __name__ == "__main__":
    main()
