import ScatterPixelIntegrator as SPI
import numpy as np
def generateScatterResultsMatrices(wavelen):
    absEff0pol, absEff90pol = np.empty(len(wavelen)),np.empty(len(wavelen))
    apertureData0pol,apertureData90pol = [],[]
    print(wavelen)

    for wnIdx,wn in enumerate(wavelen):
        absEff0pol[wnIdx],apertureData0poln = SPI.scatterPixelIntegrator(wn,0,0.65e-3,0.65e-3)
        apertureData0pol.append(apertureData0poln)

    for wnIdx,wn in enumerate(wavelen):
        absEff90pol[wnIdx],apertureData90poln = SPI.scatterPixelIntegrator(wn,90,0.65e-3,0.65e-3)
        apertureData90pol.append(apertureData90poln)

    for i, wn in enumerate(wavelen):
        np.savetxt('C:/Users/Joe/Desktop/benchmark-aperture-data-0pol %dum.dat'%wn,apertureData0pol[i])
        np.savetxt('C:/Users/Joe/Desktop/benchmark-aperture-data-90pol %dum.dat'%wn,apertureData90pol[i])

    np.savetxt('C:/Users/Joe/Desktop/benchmark-effective-aperture-0pol(%d-%dum).dat'%(min(wavelen),max(wavelen)),absEff0pol)
    np.savetxt('C:/Users/Joe/Desktop/benchmark-effective-aperture-90pol(%d-%dum).dat'%(min(wavelen),max(wavelen)),absEff90pol)