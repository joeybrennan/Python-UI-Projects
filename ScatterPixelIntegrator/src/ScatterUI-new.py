# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 14:22:07 2017

Ui controller for safari pixel integration code

@author: Joe
"""

import LoadModalData as LMD
import LoadScatterData as LSD
import IntegratePixelPerformance as IPP
import ScatterPixelIntegrator as SPI
import FindAbsorbtionModes as FAM
import BlackBodySpec as BBS
import FilterTransmission as FT
import SimulateEffectiveApertureEfficientcy as SEAF
import sys
import numpy as np
import os

from scipy.integrate import simps
from __init__ import ureg
from BaseUnits import baseUnits

from PyQt5 import uic, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

qtCreatorFile = "scatterIntegratorScale.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.simpleData.clicked.connect(self.simpleModel)
        self.realData.clicked.connect(self.realModel)
        self.BBdata.clicked.connect(self.BBspec)
        
        #Notice that an empty figure instance was added to our plotting window in the initialization method. 
        #This is necessary because our first call to changefig will try to remove a previously displayed figure,
        #which will throw an error if one is not displayed. 
        #The empty figure serves as a placeholder so the changefig method functions properly.
        fig = Figure()
        fig2 = Figure()
        fig3 = Figure()
        fig4 = Figure()
        fig5 = Figure()
        self.addmpl(fig)
        self.addmpl_2(fig2)
        self.addmpl_3(fig3)
        self.addmpl_4(fig4)
        self.addmpl_5(fig5)
     
    def BBspec(self):
        wavelen = np.linspace(float(self.min.toPlainText()),float(self.max.toPlainText()),float(self.samples.toPlainText()))*1e-6
        
        path = 'Consolidated_Filter.txt'

        BBT = float(self.BBtemp.toPlainText())
        specIr = BBS.blackBodySpec(wavelen,BBT)
        FilterCoeff = FT.filterTransmission(path,wavelen)
        
        figx = Figure()
        ax1f1 = figx.add_subplot(111)
        ax1f1.set_title('BBspec Irradiance')
        ax1f1.plot(wavelen,baseUnits(specIr),label='Simple Model')
        ax1f1.plot(wavelen,baseUnits(specIr)*FilterCoeff,label = 'After Filter')
        ax1f1.set_xlabel('Wavelength (m)')
        ax1f1.set_ylabel('Amp (%s)'%("J/m**3/s/sr"))
        ax1f1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax1f1.legend(loc='best')
        ax1f1.grid()
        #print('okay')
        self.rmmpl_3()
        self.addmpl_3(figx)
        
        
    
    def realModel(self):
        ##Load and Store data
        wavelen = np.linspace(float(self.min.toPlainText()),float(self.max.toPlainText()),float(self.samples.toPlainText()))

        apertureData0pol,apertureData90pol = [],[]
        print(wavelen)
        
        step = 100/(2*len(wavelen))
        i = 0
        self.progressBar.setValue(i)
        f = os.path.dirname(__file__) + '\\resolved data\\aperture-data-%dpol %dum.dat'
        #f = os.path.dirname(__file__) + '\\resolved data benchmark\\benchmark-aperture-data-%dpol %dum.dat'

        for wnIdx,wn in enumerate(wavelen):
            apertureData0poln = np.loadtxt(f%(0,wn))
            apertureData0pol.append(apertureData0poln)
            i=i+step
            self.progressBar.setValue(i)
            
        #absEff0pol = np.loadtxt(os.path.dirname(__file__) + '\\resolved data benchmark\\benchmark-effective-aperture-0pol(40-70um).dat')   
        absEff0pol = np.loadtxt(os.path.dirname(__file__) + '\\resolved data\\effective-aperture-0pol(40-70um).dat')   
        for wnIdx,wn in enumerate(wavelen):
            apertureData90poln = np.loadtxt(f%(90,wn))
            apertureData90pol.append(apertureData90poln)
            i=i+step
            self.progressBar.setValue(i)
        #absEff90pol = np.loadtxt(os.path.dirname(__file__) + '\\resolved data benchmark\\benchmark-effective-aperture-90pol(40-70um).dat')
        absEff90pol = np.loadtxt(os.path.dirname(__file__) + '\\resolved data\\effective-aperture-90pol(40-70um).dat')
            
        #apertureData0pol,apertureData90pol = np.asarray(apertureData0pol),np.asarray(apertureData90pol)

        ##Plot 0 deg results averaged##
        PW = np.linspace(0,10,41)
        PWx = np.linspace(0,9.75,40)
        print('okay?')
        azimuthalSum0pol = []
        for wnIdx, _ in enumerate(wavelen):
            azimuthalSum0pol.append(np.sum(apertureData0pol[wnIdx], axis = 0))
        azimuthalSum0pol = np.asarray(azimuthalSum0pol)

        
        fig0 = Figure()
        ax1f1 = fig0.add_subplot(211)
        ax1f1.set_title('Averaged Aperture Efficiency for each PW angle')
        for azimuthalSum0polN,wn in zip(azimuthalSum0pol,wavelen):
            print(np.shape(azimuthalSum0polN)[0])
            ax1f1.plot((np.linspace(0,0.25*np.shape(azimuthalSum0polN)[0],np.shape(azimuthalSum0polN)[0])),azimuthalSum0polN/37,label = '%d 0pol' %(wn))
                
        ax1f1.grid()
        ax1f1.set_xlabel('PW inclination angle (deg)')
        ax1f1.set_ylabel('Efficiency')
        ax1f1.legend(loc='best')
        
        ##Plot 90 deg results azimuthally averaged##
        azimuthalSum90pol = []
        for wnIdx, _ in enumerate(wavelen):
            azimuthalSum90pol.append(np.sum(apertureData90pol[wnIdx], axis = 0))
        azimuthalSum90pol = np.asarray(azimuthalSum90pol)
       
        ax1f2 = fig0.add_subplot(212)
        for azimuthalSum90polN,wn in zip(azimuthalSum90pol,wavelen):
            ax1f2.plot((np.linspace(0,0.25*np.shape(azimuthalSum90polN)[0],np.shape(azimuthalSum90polN)[0])),azimuthalSum90polN/37,label = '%d 90pol' %(wn))
        
        ax1f2.grid()
        ax1f2.set_xlabel('PW inclination angle (deg)')
        ax1f2.set_ylabel('Efficiency')
        ax1f2.legend(loc='best')


        ##Plot Absolute eff for 0/90deg results
        fig1 = Figure()
        ax1f3 = fig1.add_subplot(111)
        ax1f3.set_title('Aperture Efficiency for each wavelength')
        ax1f3.plot(wavelen,absEff0pol,marker = 'o',linestyle = '--',c='b',label = 'Effective Aperture 0pol')
        ax1f3.plot(wavelen,absEff90pol,marker = 'o',linestyle = '--',c='r',label = 'Effective Aperture 90pol')
        ax1f3.grid()
        ax1f3.set_xlabel('Wavelenght (um)')
        ax1f3.set_ylabel('Aperture (%s)'%("um**2*sr"))#ureg.steradian*ureg.micrometre**2))
        ax1f3.legend(loc='best')
        
        
        path = 'Consolidated_Filter.txt'
        FilterCoeff = FT.filterTransmission(path,wavelen*1e-6)
        BBT = float(self.BBtemp.toPlainText())
        specIr = BBS.blackBodySpec(wavelen*1e-6,BBT)
        
        specPowerAbsorbed0 = FilterCoeff*specIr/2*absEff0pol*ureg.steradian*ureg.mm**2
        specPowerAbsorbed90 = FilterCoeff*specIr/2*absEff90pol*ureg.steradian*ureg.mm**2

        fig3 = Figure()
        ax1f5 = fig3.add_subplot(111)
        ax1f5.set_title('Spectral Power Absorbed for each wavelength')
        ax1f5.plot(wavelen,specPowerAbsorbed0.to(ureg.kilogram*ureg.micrometer*(1/ureg.second**3)),marker = 'o',linestyle = '--',c='b',label = 'Spectral Power Abs 0pol')
        ax1f5.plot(wavelen,specPowerAbsorbed90.to(ureg.kilogram*ureg.micrometer*(1/ureg.second**3)),marker = 'o',linestyle = '--',c='r',label = 'Spectral Power Abs 90pol')
        ax1f5.set_xlabel('Wavelenght (um)')
        ax1f5.set_ylabel('Amplitude \n(%s)'%("kg*um/s**3"))#specPowerAbsorbed90.units))
        ax1f5.grid()
        ax1f5.legend(loc='best')
        

        specPowerAbsorbed = (specPowerAbsorbed0+specPowerAbsorbed90)/2
        totalPowerAbsorbed = simps(baseUnits(specPowerAbsorbed),wavelen*1e-6)
        
        self.totalPowerAbsorbed0.setText(str(totalPowerAbsorbed*ureg.watt))


        self.rmmpl_2()
        self.addmpl_2(fig0)
        self.rmmpl_4()
        self.addmpl_4(fig1)
        self.rmmpl_5()
        self.addmpl_5(fig3)
        
    def simpleModel(self):
        PW = np.linspace(0,10,41)
        wavelen = np.linspace(float(self.min.toPlainText()),float(self.max.toPlainText()),float(self.samples.toPlainText()))
        
        AppEff = SEAF.simulateEffectiveApertureEfficiency(wavelen,float(self.EOAX.toPlainText()),float(self.EOAM.toPlainText()),float(self.PAEX.toPlainText()),float(self.PAEM.toPlainText()),PW)
        
        figx = Figure()
        ax1f1 = figx.add_subplot(111)
        ax1f1.set_title('Simulated Effective Aperture Eff')

        for an,wn in zip(AppEff,wavelen):
            ax1f1.plot(PW,an,label='wavelength %dum' %wn)
        ax1f1.set_xlabel('Inclination angle')
        ax1f1.set_ylabel('Efficiency')
        ax1f1.legend(loc='best')
        ax1f1.grid()
        
        self.rmmpl()
        self.addmpl(figx)
        

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl_0.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas, 
                self.mplwindow, coordinates=True)
        self.mplvl_0.addWidget(self.toolbar)
        
    def addmpl_2(self, fig):
        self.canvas2 = FigureCanvas(fig)
        self.mplvl_2.addWidget(self.canvas2)
        self.canvas2.draw()
        self.toolbar2 = NavigationToolbar(self.canvas2, 
                self.mplwindow_2, coordinates=True)
        self.mplvl_2.addWidget(self.toolbar2)
    
    def addmpl_3(self, fig):
        self.canvas3 = FigureCanvas(fig)
        self.mplvl_3.addWidget(self.canvas3)
        self.canvas3.draw()
        self.toolbar3 = NavigationToolbar(self.canvas3, 
                self.mplwindow_3, coordinates=True)
        self.mplvl_3.addWidget(self.toolbar3)        
        
    def addmpl_4(self, fig):
        self.canvas4 = FigureCanvas(fig)
        self.mplvl_4.addWidget(self.canvas4)
        self.canvas4.draw()
        self.toolbar4 = NavigationToolbar(self.canvas4, 
                self.mplwindow_4, coordinates=True)
        self.mplvl_4.addWidget(self.toolbar4)   
        
    def addmpl_5(self, fig):
        self.canvas5 = FigureCanvas(fig)
        self.mplvl_5.addWidget(self.canvas5)
        self.canvas5.draw()
        self.toolbar5 = NavigationToolbar(self.canvas5, 
                self.mplwindow_5, coordinates=True)
        self.mplvl_5.addWidget(self.toolbar5)   
    
    def rmmpl(self):
        self.mplvl_0.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl_0.removeWidget(self.toolbar)
        self.toolbar.close()
    
    def rmmpl_2(self):
        self.mplvl_2.removeWidget(self.canvas2)
        self.canvas2.close()
        self.mplvl_2.removeWidget(self.toolbar2)
        self.toolbar2.close()

    def rmmpl_3(self):
        self.mplvl_3.removeWidget(self.canvas3)
        self.canvas3.close()
        self.mplvl_3.removeWidget(self.toolbar3)
        self.toolbar3.close()
    
    def rmmpl_4(self):
        self.mplvl_4.removeWidget(self.canvas4)
        self.canvas4.close()
        self.mplvl_4.removeWidget(self.toolbar4)
        self.toolbar4.close()
    
    def rmmpl_5(self):
        self.mplvl_5.removeWidget(self.canvas5)
        self.canvas5.close()
        self.mplvl_5.removeWidget(self.toolbar5)
        self.toolbar5.close()

    def scatterPixelIntegrator(self,wavelen,pol,width,height):
        fileMI = 'mode amplitude vs angle %dp0 um %dp0 deg.dat' %(wavelen,pol)
        fileMS = 'mode coefficients %dp0 um %dp0 deg-%d.dat'
        folderM = 'C:\\Users\\Joe\\Documents\\Python Scripts\\Scatter Pixel Code\\mode coefficients %dp0 um %dp0 deg' % (wavelen,pol)
        fileS = 'sron_rect_gap%dum_s11_abso400_%s.dat'
        folderS = 'C:\\Users\\Joe\\Documents\\Python Scripts\\Scatter Pixel Code\\Scatter Data'
        
        ApertureArea = width*height
        
        ##WORKING
        Amps,modelist,PW,Azi = LMD.loadModalData(fileMI,fileMS,folderM,wavelen,pol)
        print('Modal Data Loaded')
        ##WORKING
        S11 = LSD.loadScatterData(fileS,folderS,wavelen)
        print('Scatter Data Loaded')
        ##WORKING
        AbosrbtionChannels = FAM.findAbsorptionModes(S11)
    #    return PW,Azi,ApertureArea,modelist,Amps,AbosrbtionChannels
        print('AbsorbtionChannels got')
        absEff, RRR = IPP.integratePixelPerformance(PW,Azi,ApertureArea,modelist,Amps,AbosrbtionChannels)
        print('done')
        return absEff, RRR
    #    for RRRm in RRR:
    #        plt.plot(PW,RRRm)
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    window = Main()
    window.show()
    app.exec_()