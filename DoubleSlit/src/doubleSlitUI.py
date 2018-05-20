import generateAM as genAM
import numpy as np
import sys

from PyQt5 import uic, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

qtCreatorFile = "doubleslitui.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.plotField.clicked.connect(self.plotfield)

        
        #Notice that an empty figure instance was added to our plotting window in the initialization method. 
        #This is necessary because our first call to changefig will try to remove a previously displayed figure,
        #which will throw an error if one is not displayed. 
        #The empty figure serves as a placeholder so the changefig method functions properly.
        fig = Figure()
        self.addmpl(fig)

     
    
    def plotfield(self):
        wavelen = float(self.wavelen.toPlainText())
        modenum = int(self.modeNum.toPlainText())
        Zin = float(self.z.toPlainText())
        
        x,ET = genAM.doubleSlit(wavelen, modenum, Zin)
        
        figx = Figure()
        ax1f1 = figx.add_subplot(111)
        ax1f1.set_title('Beam Pattern')

        ax1f1.plot(x,np.abs(ET)**2,label='Beam Pattern at %s m' %Zin)
        ax1f1.set_xlabel('x [m]')
        ax1f1.set_ylabel('Intensity')
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
        
    def rmmpl(self):
        self.mplvl_0.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl_0.removeWidget(self.toolbar)
        self.toolbar.close()
    

    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    window = Main()
    window.show()
    app.exec_()
    