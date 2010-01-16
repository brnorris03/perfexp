#!/usr/bin/python

from math import *
from params import * 
from analysis.tools.tau import PerfExplorer 
from analysis.interfaces import AbstractModel 

class RA(AbstractModel):
    '''Model for RandomAccess'''

    def __init__(self):
        pass
    
    def validate(self, params):

        rc = float(modelparams[0])
        lc = float(modelparams[1])
        P = int(params[0])
        numupdates = float(modelparams[2])
        
        if P == 0:
            remoteupdates = 0
            localupdates = numupdates
        else:
            remoteupdates = ((float)(P-1)/P) * numupdates
            localupdates = numupdates - remoteupdates

        time = (remoteupdates * rc) + (localupdates * lc)

        if DEBUG == 1:
            print 'Time: ', time

        return time


