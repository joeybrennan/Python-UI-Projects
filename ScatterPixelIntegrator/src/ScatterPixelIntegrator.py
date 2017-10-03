# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 14:37:02 2017

Control for find Scatter Pixel intergator, takes in wavelength range
polarisation angles and aperture dimensions

returns: absolute Eff, Apeture Eff for each Azi angle

@author: Joe Brennan
"""

import LoadModalData as LMD
import LoadScatterData as LSD
import IntegratePixelPerformance as IPP
import FindAbsorbtionModes as FAM

def scatterPixelIntegrator(wavelen,pol,width,height):
    fileMI = 'mode amplitude vs angle %dp0 um %dp0 deg.dat' %(wavelen,pol)
    fileMS = 'mode coefficients %dp0 um %dp0 deg' %(wavelen,pol) + '-%d.dat' 
    folderM = 'C:\\Users\\Joe\\Documents\\Python Scripts\\Scatter Pixel Code\\BenchMark Tests\\mode coefficients no aperture %dp0 um %dp0 deg' % (wavelen,pol)
    fileS = 'sron_rect_gap%dum_s11_abso400_%s.dat'
    folderS = 'C:\\Users\\Joe\\Documents\\Python Scripts\\Scatter Pixel Code\\Scatter Data'
    
    ApertureArea = width*height
    
    ##WORKING
    amps,modeList,inclinationAngles,azimuthalAngles = LMD.loadModalData(fileMI,fileMS,folderM)
    print('Modal Data Loaded')

#    ##WORKING
    S11 = LSD.loadScatterData(fileS,folderS,wavelen)
    print('Scatter Data Loaded')
#    ##WORKING
    AbosrbtionChannels = FAM.findAbsorptionModes(S11)
##    return PW,Azi,ApertureArea,modelist,Amps,AbosrbtionChannels
    print('AbsorbtionChannels got')
    simsAbsoluteEff,apertureData = IPP.integratePixelPerformance(amps,modeList,inclinationAngles,azimuthalAngles,AbosrbtionChannels,ApertureArea)
    print('done')
    return simsAbsoluteEff,apertureData
