#!/usr/bin/python

from params import *
import util.setup
from analysis.tools.tau import PerfExplorer

def main():

    util.setup.setPythonPath()     # automatically set the Python search path
    
    analysis = PerfExplorer()
    analysis.runAnalysis()

if __name__ == "__main__":

    main()
