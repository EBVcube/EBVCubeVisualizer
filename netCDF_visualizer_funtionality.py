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
        self.btn_remove_sel.clicked.connect(self.removeSelection)
        
        """Here is the place for set stzlesheet"""
        #self.btn_plot.setStyleSheet("backgrou")

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
        self.tree_data.clear()
        #we remove the information from the listWidget
        #self.column_data.clear()

    def removeSelection(self):
        """this function remove the selection in the tree widget"""
        #we remmove the selectec TopLevelItems from the tree widget
        for item in self.tree_data.selectedItems(): 
            self.tree_data.takeTopLevelItem(self.tree_data.indexOfTopLevelItem(item))


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
            ncFileName = os.path.basename(path)
            #We get the title of the netCDF file
            ncFileTitle = ncFile.title
            #convert file name and file title into a QTreeWidgetItem
            top_level = QTreeWidgetItem([ncFileName, ncFileTitle])
            #we get the variables of the netCDf file
            ncFileVariablesName = list(ncFile.variables.keys())
            #we get the groups of the file
            ncFileGroupsName = list(ncFile.groups.keys())
  
            
            #we set the top of the tree that it is the name od the file
            self.tree_data.addTopLevelItem(top_level)
            
            #we get the variables of the file and show then as well as the long name in the tree
            for i in range(len(ncFileVariablesName)):
                child = QTreeWidgetItem([ncFileVariablesName[i], ncFile.variables[ncFileVariablesName[i]].long_name])
                top_level.addChild(child)
        
            #we show the groups of the file in the QTreeWidgetite
            for i in range(len(ncFileGroupsName)):
                child = QTreeWidgetItem([ncFileGroupsName[i], ncFileGroupsName[i]])
                top_level.addChild(child)
                
                #we get the groups of the groups
                ncFileGroupsName2 = list(ncFile.groups[ncFileGroupsName[i]].groups.keys())
               
                #we show the groups of the groups in the QTreeWidgetite
                for j in range(len(ncFileGroupsName2)):
                    child2 = QTreeWidgetItem([ncFileGroupsName2[j], ncFileGroupsName2[j]])
                    child.addChild(child2)
                   
                    #we get the variables of the groups of the groups
                    ncFileVariablesName2 = list(ncFile.groups[ncFileGroupsName[i]].groups[ncFileGroupsName2[j]].variables.keys())
                   
                    #we show the variables of the groups of the groups in the QTreeWidgetite an set the lon name of the variables
                    for k in range(len(ncFileVariablesName2)):
                        child3 = QTreeWidgetItem([ncFileVariablesName2[k]])
                        child2.addChild(child3)
              
                
                #we get the variables of the groups
                ncFileGroupsVariablesName = list(ncFile.groups[ncFileGroupsName[i]].variables.keys())
                
            
                #we show the variables of the groups in the QTreeWidgetite and set the long name of the variables
                for j in range(len(ncFileGroupsVariablesName)):
                    longNameVariables = ncFile.groups[ncFileGroupsName[i]].variables[ncFileGroupsVariablesName[j]].long_name
                    child4 = QTreeWidgetItem([ncFileGroupsVariablesName[j],longNameVariables])
                    child.addChild(child4)
                    

                    




        

            # #we set the dimensions in the ListWidget
            # self.column_data.addItems(ncFileDimensions)
            # #we set the variables in the ListWidget
            # self.column_data.addItems(ncFileVariables)
            
           

                      
            #we close the netCDF file
            ncFile.close()
            #remove the path from the text space
            self.text_set.clear()
            
    def plotNetCDF(self):
        """This function plots the netCDF file"""
        
