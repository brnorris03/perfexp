#!/usr/bin/python

from XeonMeasurementEnv import *
from Plotter import *

def main():

    vm = XeonMeasurementEnv()
    plotter = Plotter()
    xdata,ydata = vm.validateModel()
    plotter.generatePlot(xdata,ydata)

if __name__ == "__main__":

    main()
