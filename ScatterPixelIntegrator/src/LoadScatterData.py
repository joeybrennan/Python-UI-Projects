# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 17:00:30 2017

This program parses the real and imag scatter files and combines them
into the approriate S11 matrix

returns: S11

@author: Joe
"""

import pandas as pd
import numpy as np
import os

def loadScatterData(file,folder,wavelen):
    
    real = getRealData(os.path.join(folder,file %(wavelen,'real')))
    imag = getImagData(os.path.join(folder,file %(wavelen,'imag')))
    
    S11 = (real+np.multiply(imag,1j))
    
    return S11
    
def getRealData(path):
    dataR = pd.read_csv(path,delimiter='\t',header=None)
    dataR = dataR.as_matrix()
    return dataR
    
def getImagData(path):
    dataI = pd.read_csv(path,delimiter='\t',header=None)
    dataI = dataI.as_matrix()
    return dataI