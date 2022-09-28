from PyQt5 import uic

myGUI = uic.loadUi(r"I:\biocon\Emmanuel_Oceguera\netCDFVisualizationPlugin\netCDF_visualizer.ui")
myGUI.show()

def importData():
    #print("ok")
    path = QFileDialog.getOpenFileName(None,"select netCDF file", filter="*.nc")[0]
    #print(path)
    
    #to set the path in the text space 
    myGUI.text_set.setText(path)

myGUI.btn_inputFile.clicked.connect(importData)

def removePath():
    #print("ok")
    myGUI.text_set.clear()

myGUI.btn_remove.clicked.connect(removePath)

def loadData():
   print("ok") 



myGUI.btn_load.clicked.connect(loadData)

def closePlugin():
    #close the Plugin
    #print ("ok")
    myGUI.close()
    
myGUI.btn_closePlugin.clicked.connect(closePlugin)