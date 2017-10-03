# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 12:48:07 2017

This program uses SVD to obtain the absorbtion modes for the
S11 matrix of scatter data

returns: absorbtionChannels

@author: Joe
"""

import numpy as np

def findAbsorptionModes(scatter):
    ##Preform SVD on scatter S11 data
    U,s,V = np.linalg.svd(scatter,full_matrices=True)
    U = np.transpose(U)
    
    absorbtionChannels = []
    threshold = 1e-10
    absorbmode = ()
    for i in range(np.shape(U)[0]):
        sn = s[i]
        vr = U[i]
        
        if threshold < sn < 1-threshold:
            absorb = 1-sn**2
            absorbmode = (absorb,vr)
            absorbtionChannels.append(absorbmode)
        
    return absorbtionChannels
            
            