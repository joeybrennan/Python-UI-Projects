# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 16:39:22 2017

@author: Joe
"""

import pandas as pd
import numpy as np

def filterTransmission(path, wavelen):
    data = pd.read_csv(path,sep='\t',header=None)
    data = data.as_matrix()   
    data=data.transpose()
    FilterCoeff = np.interp(wavelen*1000,data[0],data[1])
    
    return FilterCoeff