# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 18:57:00 2017

    UI file for inspecting description headers of SCATTER zip files.
    Allows user to remove unwanted or duplicate files.

@author: Joe Brennan
"""

import sys
import os
import zipfile
from PyQt5 import QtCore, QtGui, uic, QtWidgets


qtCreatorFile = "ZipFileViewer.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

        
class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        QtWidgets.QAbstractItemView
        #signal and slots for the ui
        self.folderselect.clicked.connect(self.sFold)
        self.zipfiles.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.zipview.clicked.connect(self.showDescription)
        self.remove.clicked.connect(self.removeSelected)
        
    def sFold(self):
        #Populates the list with the zip files present in the dir
        self.folder.setText(QtWidgets.QFileDialog.getExistingDirectory())
        for f in os.listdir(self.folder.toPlainText()):
            if os.path.isfile(os.path.join(self.folder.toPlainText(),f)):
                self.zipfiles.addItem(f)

    
    def showDescription(self,item):
        self.description.clear()
        #Gets the description file from the scatter.zip
        f = self.zipfiles.selectedItems()
        for fn in f:
            print(fn.text())
            path = os.path.join(self.folder.toPlainText(),fn.text())
            zf = zipfile.ZipFile(path,'r')
            self.description.append(str(zf.read("DESCRIPTION.txt")))
        
    def removeSelected(self):
        #removes the desired file, quick message to double check.
        reply = QtWidgets.QMessageBox.question(self, 'Alert!!', "Do you wish to remove this Zip file?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        
        if reply == QtWidgets.QMessageBox.Yes:
            f = self.zipfiles.currentItem().text()
            self.zipfiles.takeItem(self.zipfiles.row(self.zipfiles.currentItem()))
            path = os.path.join(self.folder.toPlainText(),f)
            os.remove(path)
        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    window = Main()
    window.show()
    app.exec_()