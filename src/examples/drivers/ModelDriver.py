#!/usr/bin/python

from me.platforms.xeon import Generic as XeonMeasurementEnv
from examples.models.logp_FT import FT
from vis.tools.pylab import Plotter

def main():

    
    vm = XeonMeasurementEnv()
    plotter = Plotter()
    model = FT()
    xdata,ydata = vm.validateModel(model)
    plotter.generatePlot(xdata,ydata)
    plotter.generateMergedPlot(xdata,ydata)

if __name__ == "__main__":

    main()
