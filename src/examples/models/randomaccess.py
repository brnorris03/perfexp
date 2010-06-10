#!/usr/bin/python

from math import *
from analysis.tools.tau import PerfExplorer 
from analysis.interfaces import AbstractModel 
from examples.models.params import RAParams

class RA(AbstractModel):
    '''Model for RandomAccess'''

    def __init__(self):
        pass
    
    def validate(self, params):

        rc = float(RAParams.modparams['rc']
        lc = float(RAParams.modparams['lc']
        P = int(params[0])
        numupdates = float(RAParams.modparams['numupdates'])
        
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


