# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 15:03:21 2017

@author: Joe
"""
import numpy as np
import scipy.constants as spc
from __init__ import ureg,Q_

def blackBodySpec(wavelens,BBtemp):
    
    wavelens = wavelens*ureg.meter
    BBtemp = BBtemp*ureg.kelvin
    c = spc.speed_of_light*ureg.meter/ureg.sec
    h = spc.Planck*ureg.joule*ureg.sec
    k = spc.Boltzmann*ureg.joule/ureg.kelvin
    
    specIr = np.zeros((len(wavelens)))
    print(len(specIr))
    for i,wn in enumerate (wavelens):
        result = ((2*h*c**2)/(wn**5))*(1/(((np.exp((h*c)/(wn*k*BBtemp)))-1)))
        specIr[i] = result.to_base_units().magnitude

    return specIr*result.units/ureg.steradian