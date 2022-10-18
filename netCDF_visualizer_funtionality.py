'''
/****************************************************************************************
* This is a python script for visualizing netCDF files using PyQt5 and matplotlib
* 
* The script is based on the QGIS plugin template by Gispo
* 
* 
****************************************************************************************/

/****************************************************************************************
* The program is free software; you can redistribute it and/or modify                   
* it under the terms of the GNU General Public License as published by                  
* the Free Software Foundation; either version 2 of the License, or                              
* at your option) any later version.                                                     
* 
* The script is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
* without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
* See the GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License along with this program. 
* If not, see http://www.gnu.org/licenses/.
****************************************************************************************/
'''
#we import the impotant libraries and modules
#always import the libraries and modules at the top of the code

from json import load
from msilib.schema import tables
from PyQt5.QtCore import *  
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

#we want to work with the os module
import os
#to import general tools from QGIS we need the qgis.core module
from qgis.core import *
#for loading the netCDF files we need the netCDF4 module
try:
   from pip import main as pipmain
except ImportError:
   from pip._internal import main as pipmain

try:
   import netCDF4 as nc
except ImportError:
   pipmain(['install', 'netCDF4'])
   import netCDF4 as nc
   from netCDF4 import Dataset

#we need the matplotlib module to plot the data
#try: 
#    import matplotlib
#except ImportError:
#    pipmain(['install', 'matplotlib'])
#    import matplotlib


#we create the path to the ui file
#Path to the Ordner where the ui file is
ncvPath = os.path.dirname(__file__) #the comand dirname gives the path to the directory where the file is
#path to the ui file
#dosn't matter where the ui file is located in the directory 
uiPath = os.path.join(ncvPath, 'netCDFVisualizer.ui')

#TWO CLASES#    
# WIDEGT is a class for the GUI
# BASE is a PyQt5 class to insatalize the GUI
WIDGET, BASE = uic.loadUiType(uiPath)

class maskAndFuntionality (BASE, WIDGET):
    """Class for the mask and the funtionality of the netCDFVisualizer Plugin"""
    def __init__(self, iface):
        #self is GUI and mask
        QDialog.__init__(self, iface.mainWindow())
        self.setupUi(self)
        #self ist our GUI
        #the GUI is built in the running of QGIS in the current session (using the iface)
        """ Here is the place for the Clicked Signal"""
        self.btn_closePlugin.clicked.connect(self.closePlugin)
        self.btn_inputFile.clicked.connect(self.importData)
        self.btn_remove.clicked.connect(self.removePath)
        self.btn_load.clicked.connect(self.loadNetCDF)


    def closePlugin(self):
        """This function closes the plugin"""
        #we close the plugin
        self.close()

    def importData(self):
        """This function imports the netCDF file"""
        #we get the path to the netCDF file
        path = QFileDialog.getOpenFileName(None,"select netCDF file", filter="*.nc")[0]
        #we set the path in the text space
        self.text_set.setText(path)

    def removePath(self):
        """This function removes the path from the text space"""
        #we remove the path from the text space
        self.text_set.clear()
        #we remove the information from the table widget
        self.tree_data.clearContents()
        #we remove the information from the listWidget
        self.column_data.clearContents()


    


    def loadNetCDF(self):
        """This function loads the netCDF file"""
        #we get the path from the text space
        if self.text_set.text()=="": #if the text space is empty
            QmessageBox.warning(None, "Warning", "Please select a netCDF file") #we show a warning
        else: #if the text space is not empty
            path = self.text_set.text() #we get the path from the text space
            #we load the netCDF file
            ncFile = nc.Dataset(path, 'r', format='NETCDF4')
            #we get the name of the netCDF file to show it in the GUI
            ncFileName = QTreeWidgetItem([os.path.basename(path)])
            #We get the title of the netCDF file
            ncFileTitle = QTreeWidgetItem([ncFile.title])
            #we get the variables of the netCDf file
            ncFileVariables = ncFile.variables
        
            #we set the top of the tree that it is the name od the file
            self.tree_data.addTopLevelItem(ncFileName)
            
               
            #we set the dimensions in the ListWidget
            self.column_data.addItems(ncFileDimensions)
            #we set the variables in the ListWidget
            self.column_data.addItems(ncFileVariables)
            
        

          
            #we close the netCDF file
            ncFile.close()

