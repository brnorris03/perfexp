#!/usr/bin/python

from params import *
import util.config
from analysis.tools.tau import PerfExplorer

def main():

    util.config.setPythonPath()     # automatically set the Python search path
    
    analysis = PerfExplorer()
    analysis.runAnalysis()

if __name__ == "__main__":

    main()
