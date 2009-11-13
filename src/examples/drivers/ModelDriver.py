#!/usr/bin/python

from me.platforms.xeon import Generic as XeonMeasurementEnv
from examples.models.logGP_FT import LogGPFT
from vis.tools.pylab import Plotter

def main():

    
    vm = XeonMeasurementEnv()
    plotter = Plotter()
    model = LogGPFT()
    xdata,ydata = vm.validateModel(model)
    plotter.generatePlot(xdata,ydata)

if __name__ == "__main__":

    main()
