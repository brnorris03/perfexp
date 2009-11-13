#!/usr/bin/python

from me.platforms.xeon import Generic as XeonMeasurementEnv
from vis.tools.pylab import Plotter

def main():

    
    vm = XeonMeasurementEnv()
    plotter = Plotter()
    xdata,ydata = vm.validateModel()
    plotter.generatePlot(xdata,ydata)

if __name__ == "__main__":

    main()
