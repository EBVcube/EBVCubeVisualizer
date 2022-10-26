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
import matplotlib.pyplot as plt


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
        self.btn_plot.clicked.connect(self.plotEbvCube)
        
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
        #we remove the information from the QtextBrowser
        self.text_info.clear()
        

    def removeSelection(self):
        """this function remove the selection in the tree widget"""
        #we remmove the selectec TopLevelItems from the tree widget
        for item in self.tree_data.selectedItems(): 
            self.tree_data.takeTopLevelItem(self.tree_data.indexOfTopLevelItem(item))
        else:
            self.text_info.clear()
            
        


    def loadNetCDF(self):
        """This function loads the netCDF file and shows the variables, groups and the variables of the gorups in the QTreeWidget"""
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
            
        
            #we show the groups of the file in the QTreeWidgetite
            for i in range(len(ncFileGroupsName)):
                longNameGroups = ncFile.groups[ncFileGroupsName[i]].long_name
                child = QTreeWidgetItem([ncFileGroupsName[i], longNameGroups])
                top_level.addChild(child)
                
                #we get the groups of the groups
                ncFileGroupsName2 = list(ncFile.groups[ncFileGroupsName[i]].groups.keys())
               
                #we show the groups of the groups in the QTreeWidgetite
                for j in range(len(ncFileGroupsName2)):
                    longNameGroups2 = ncFile.groups[ncFileGroupsName[i]].groups[ncFileGroupsName2[j]].long_name
                    child2 = QTreeWidgetItem([ncFileGroupsName2[j], longNameGroups2])
                    child.addChild(child2)
                        
                    #we get the variables of the groups of the groups
                    ncFileVariablesName2 = list(ncFile.groups[ncFileGroupsName[i]].groups[ncFileGroupsName2[j]].variables.keys())
                   
                    #we show the variables of the groups of the groups in the QTreeWidgetite an set the lon name of the variables
                    for k in range(len(ncFileVariablesName2)):
                        longNameVariables2 = ncFile.groups[ncFileGroupsName[i]].groups[ncFileGroupsName2[j]].variables[ncFileVariablesName2[k]].long_name
                        child3 = QTreeWidgetItem([ncFileVariablesName2[k], longNameVariables2])
                        child2.addChild(child3)

                    #we get the attributes of the variables of the groups of the groups and show them in the QTextBrowser if the variable is clicked
                    if child3.isSelected():
                        ncFileVariablesName2Attributes = list(ncFile.groups[ncFileGroupsName[i]].groups[ncFileGroupsName2[j]].variables[ncFileVariablesName2[k]].ncattrs())
                        for l in range(len(ncFileVariablesName2Attributes)):
                            ncFileVariablesName2AttributesValue = ncFile.groups[ncFileGroupsName[i]].groups[ncFileGroupsName2[j]].variables[ncFileVariablesName2[k]].getncattr(ncFileVariablesName2Attributes[l])
                            self.text_info.append(ncFileVariablesName2Attributes[l] + ": " + str(ncFileVariablesName2AttributesValue))

                
                #we get the variables of the groups
                ncFileGroupsVariablesName = list(ncFile.groups[ncFileGroupsName[i]].variables.keys())
                
            
                #we show the variables of the groups in the QTreeWidgetite and set the long name of the variables
                for j in range(len(ncFileGroupsVariablesName)):
                    longNameVariables = ncFile.groups[ncFileGroupsName[i]].variables[ncFileGroupsVariablesName[j]].long_name
                    child4 = QTreeWidgetItem([ncFileGroupsVariablesName[j],longNameVariables])
                    child.addChild(child4)
            
            #expand all the data 
            self.tree_data.expandAll()
            

            """ here we are gonna show all information into the GUI"""
            #we get the attributes of the file and show them in the QTextBrowser when the file is loaded
            ncFileAttributes = list(ncFile.ncattrs())
            for i in range(len(ncFileAttributes)):
                ncFileAttributesValue = ncFile.getncattr(ncFileAttributes[i])
                self.text_info.append(ncFileAttributes[i] + ": " + str(ncFileAttributesValue)) 

        
            #we close the netCDF file
            ncFile.close()
            
            
            
    def plotEbvCube(self):
        """This function plots the EBV cube if the user select the EBV cube"""
        #we get the selected item from the tree widget
        item = self.tree_data.selectedItems()
        #we get the name of the selected item
        name = item[0].text(0)
        #we get the path of the netCDF file
        path = self.text_set.text()
        #we load the netCDF file
        ncFile = nc.Dataset(path, 'r', format='NETCDF4')
        #we get the EBV cube
        ebvCube = ncFile.variables[name][:]
        #we plot the EBV cube
        plt.imshow(ebvCube)
        plt.show()
        #we close the netCDF file
        ncFile.close()
        
