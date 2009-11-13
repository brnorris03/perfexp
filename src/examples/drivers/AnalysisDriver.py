#!/usr/bin/python

from params import *
from analysis.tools.tau import PerfExplorer

def main():
    
    analysis = PerfExplorer()
    analysis.runAnalysis()

if __name__ == "__main__":

    main()
