#!/usr/bin/python

from me.platforms.xeon import Generic as XeonMeasurementEnv
from me.platforms.aix import BluePrint as AIXMeasurementEnv
from examples.models.logp_FT import FT
from examples.models.rarma import RARMA
from vis.tools.pylab import Plotter
from examples.models.params import RARMAParams
from analysis.params import ANSParams
from me.params import MEParams
from examples.models.params import GENParams

def main():

    modParams = RARMAParams()
    modParams._processConfigFile()

    ansParams = ANSParams()
    ansParams._processConfigFile()

    meParams = MEParams()
    meParams._processConfigFile()

    genParams = GENParams()
    genParams._processConfigFile()
    
    vm = AIXMeasurementEnv()
    plotter = Plotter()
    model = RARMA()
    xdata,ydata = vm.validateModel(model)
    plotter.generatePlot(xdata,ydata)
    plotter.generateMergedPlot(xdata,ydata)

if __name__ == "__main__":

    main()
