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
from datetime import datetime
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
from qgis.utils import iface

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
#we need gdal to work with the raster data 
from osgeo import osr, gdal, ogr
#we ned the numpy module to work with the data
import numpy as np


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
        self.btn_load.clicked.connect(self.setMapData)
        self.btn_remove_sel.clicked.connect(self.removeSelection)
        #here we set the clicked signal for the tree widget
        self.tree_data.itemClicked.connect(self.showInfo)
        self.btn_plot.clicked.connect(self.displayData)
        
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
        self.text_set.clear()
        self.tree_data.clear()
        self.text_info.clear()
        self.cbox_entity.clear()
        self.cbox_time.clear()
        self.cbox_scenarios.clear()
        self.cbox_metric.clear()

    def removeSelection(self):
        """this function remove the selection in the tree widget"""
        #if the top level item is selected we remove the Item and the children as well text_info, cbox_entity and cbox_time
        if self.tree_data.currentItem().parent() == None:
            self.tree_data.takeTopLevelItem(self.tree_data.indexOfTopLevelItem(self.tree_data.currentItem()))
            self.text_info.clear()
            self.cbox_entity.clear()
            self.cbox_time.clear()
            self.cbox_scenarios.clear()
            self.cbox_metric.clear()
        #if the child item is selected we don't remove anything
        elif self.tree_data.currentItem() == None:
            pass

        else:
            pass
            

    def loadNetCDF(self):
        """This function loads the netCDF file and shows the variables, groups and the variables of the gorups in the QTreeWidget"""
        #we get the path from the text space
        if self.text_set.text()=="": #if the text space is empty
            QmessageBox.warning(None, "Warning", "Please select a netCDF file") #we show a warning
       
        else: #if the text space is not empty
            path = self.text_set.text() #we get the path from the text space
            ncFile = nc.Dataset(path, 'r', format='NETCDF4')
            ncFileName = os.path.basename(path)
            ncFileTitle = ncFile.title
            #convert file name and file title into a QTreeWidgetItem
            top_level = QTreeWidgetItem([ncFileName, ncFileTitle])
            #we get the variables of the netCDf file
            ncFileVariablesName = list(ncFile.variables.keys())
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

                #we get the variables of the groups
                ncFileGroupsVariablesName = list(ncFile.groups[ncFileGroupsName[i]].variables.keys())
                
                #we show the variables of the groups in the QTreeWidgetite and set the long name of the variables
                for j in range(len(ncFileGroupsVariablesName)):
                    longNameVariables = ncFile.groups[ncFileGroupsName[i]].variables[ncFileGroupsVariablesName[j]].long_name
                    child4 = QTreeWidgetItem([ncFileGroupsVariablesName[j],longNameVariables])
                    child.addChild(child4)
        
            
            #expand all the data 
            self.tree_data.expandAll()
            ncFile.close() #close the file
            
    def setMapData(self):
        """This function sets the entities, time, scenarios and metrics in the QComboBox"""
        #we clear the QComboBox
        self.cbox_entity.clear()
        self.cbox_time.clear()
        self.cbox_scenarios.clear()
        self.cbox_metric.clear()
        
        #we get the path from the text space
        path = self.text_set.text()
        ncFile = nc.Dataset(path, 'r', format='NETCDF4') 

        groups = list(ncFile.groups.keys()) #we get the metrics (name of the groups)
        groupsOfGroups = list(ncFile.groups[groups[0]].groups.keys()) #we get the scenarios(name of the groups of the groups)


        #set scenario and metric in the QComboBox  
        #if there is just groups we set the groups in the cbox_metric 
        self.cbox_metric.addItems(groups)
        self.cbox_scenarios.addItem("not scenarios")
        self.cbox_scenarios.setEnabled(False)
        
        if len(groupsOfGroups)>0:
            self.cbox_scenarios.setEnabled(True)
            self.cbox_scenarios.clear()
            self.cbox_scenarios.addItems(groups)
            self.cbox_metric.clear()
            self.cbox_metric.addItems(groupsOfGroups)
        else:
            pass

        #here we are gonna get the entities and the time of the netCDF file and set them into a QComboBox if the top level is clicked
        #we get the time of the netCDF file
        time = ncFile.variables['time']
        timeUnits = time.units
        timeCalendar = time.calendar
        time = nc.num2date(time[:], timeUnits, timeCalendar)

        #we set the time into the QComboBox
        self.cbox_time.clear()
        self.cbox_time.addItems([str(i) for i in time])
        
        #we get the entities
        self.cbox_entity.clear()
        entities = ncFile.variables['entity']
        entityScope = entities.ebv_entity_scope.split(',')
        numberOfEntities = len(entities)
        #we set the entity_scope and the number of the entity into the QComboBox
        #self.cbox_entity.addItems([entityScope[i] + " " + str(i) for i in range(numberOfEntities)])
        
        #we set the entities into the QComboBox
        self.cbox_entity.addItems(entityScope)


        #we close the netCDF file
        ncFile.close()
        
    def showInfo(self):
        """this function shows first the name of the file and the global attributes and then if a varible is clicked delete the info and add the attributes of the selected variable"""
        self.text_info.clear()
        #we get the path from the text space
        path = self.text_set.text()
        ncFile = nc.Dataset(path, 'r', format='NETCDF4')
        ncFileName = os.path.basename(path)
        ncFileTitle = ncFile.title
        ncFileGlobalAttributes = list(ncFile.ncattrs())
        
        #when we click on the top level item we show the name of the file, title and the global attributes
        if self.tree_data.currentItem().parent() == None:
            self.text_info.clear()
            self.text_info.append("File name: " + ncFileName)
            self.text_info.append("Title: " + ncFileTitle)
            self.text_info.append("Global attributes:")
            for i in range(len(ncFileGlobalAttributes)):
                self.text_info.append("-- " + ncFileGlobalAttributes[i] + ": " + str(ncFile.getncattr(ncFileGlobalAttributes[i])))
                
        #when we click on a group we show the name of the group and the attributes of the group and if we click on a variable of the group we show the attributes of the variable
        elif self.tree_data.currentItem().parent().parent() == None:
            self.text_info.clear()
            self.text_info.append("File name: " + ncFileName)
            self.text_info.append("Title: " + ncFileTitle)
            self.text_info.append("Group name: " + self.tree_data.currentItem().text(0))
            self.text_info.append("Long name: " + self.tree_data.currentItem().text(1))
            self.text_info.append("Attributes:")
            for i in range(len(ncFile.groups[self.tree_data.currentItem().text(0)].ncattrs())):
                self.text_info.append("-- " + ncFile.groups[self.tree_data.currentItem().text(0)].ncattrs()[i] + ": " + str(ncFile.groups[self.tree_data.currentItem().text(0)].getncattr(ncFile.groups[self.tree_data.currentItem().text(0)].ncattrs()[i])))   
        
        #when we click on a variable of the group and the attributes of the varibales
        else:
            self.text_info.append("File name: " + ncFileName)
            self.text_info.append("Title: " + ncFileTitle)
            self.text_info.append("Variable name: " + self.tree_data.currentItem().text(0))
            self.text_info.append("Long name: " + self.tree_data.currentItem().text(1))
            self.text_info.append("Attributes:")
            variableAttributes = list(ncFile.groups[self.tree_data.currentItem().parent().text(0)].variables[self.tree_data.currentItem().text(0)].ncattrs())
            for i in range(len(variableAttributes)):
                self.text_info.append("-- " + variableAttributes[i] + ": " + str(ncFile.groups[self.tree_data.currentItem().parent().text(0)].variables[self.tree_data.currentItem().text(0)].getncattr(variableAttributes[i])))

        #we close the netCDF file
        ncFile.close()


    def displayData(self):
        """this fuction get the data of each ebv_cube and add it to the map"""
        path = self.text_set.text() #we get the path from the text space
        ncFile = nc.Dataset(path, 'r', format='NETCDF4') #we are gonna open the nedCDF file with the netCDF4 library
        ncFileName = os.path.basename(path) #We get the name of the netCDF file to show it in the GUI
        #get part of the name of the netCDF file
        ncFileName = ncFileName.split('_')
        ncFileName = ncFileName[0] + '_' + ncFileName[1] + '_' + ncFileName[2]
        nameOfRasterLayer =  ncFileName + "_entity: " + self.cbox_entity.currentText() + "_time: " + self.cbox_time.currentText() #we get the name of the raster layer
        
        #time
        #we get the time 
        time = ncFile.variables['time']
        timeUnits = time.units 
        timeCalendar = time.calendar
        time = nc.num2date(time[:], timeUnits, timeCalendar)
        time = [str(i) for i in time] #we have to convert the time into a string
        max_time = len(time) #we get the length of the time
      
        #time selected in the QComboBox
        timeSelected = self.cbox_time.currentText()
        timeIndex = time.index(timeSelected) #we get the index of the time selected
        

        #Entity
        #we get the entities
        entity = ncFile.variables['entity']
        entityScope = entity.ebv_entity_scope.split(',') #we get the name of the entities

        #entity selected in the QComboBox
        entitySelected = self.cbox_entity.currentText()
        entityIndex = entityScope.index(entitySelected) #we get the index of the entity selected
        
        
        #get the scenarios and the metrics from the interface
        #scenarios
        scenarioSelected = self.cbox_scenarios.currentText()
        scenarioIndex = self.cbox_scenarios.currentIndex()
        #metrics
        metricSelected = self.cbox_metric.currentText()
        metricIndex = self.cbox_metric.currentIndex()
        
        uri = r'NETCDF:"'+ path + '":' + metricSelected + '/ebv_cube'
        
        #if there just metrics and no scenarios we have to create a uri with the metric selected in the QComboBox
        # if scenarioIndex == 0:
        #     uri = r'NETCDF:"'+ path + '":' + metricSelected + '/ebv_cube'
        # else:
        #     uri = r'NETCDF:"'+ path + '":'+ scenarioSelected + '/' + metricSelected + '/ebv_cube'
        
      

        #load the raster layer into the QGIS canvas
        rasterLayer = QgsRasterLayer(uri, nameOfRasterLayer, "gdal")
        print(rasterLayer.isValid())
        
        
        #calculate the band number
        band = (entityIndex-1)*max_time+ timeIndex
        
        
        #get the min and the max value of the band
        dp = rasterLayer.dataProvider()
        stats = dp.bandStatistics(band)
        min = stats.minimumValue
        max = stats.maximumValue

        #build the color ramp
        colorRamp = QgsColorRampShader(min, max)
        colorRamp.setColorRampType(QgsColorRampShader.Interpolated)
        colorRamp.setColorRampItemList([QgsColorRampShader.ColorRampItem(min, QColor(0, 0, 255)), 
                                        QgsColorRampShader.ColorRampItem(max, QColor(255, 0, 0))])
        #build the shader
        shader = QgsRasterShader()
        shader.setRasterShaderFunction(colorRamp)

        #build the renderer
        renderer = QgsSingleBandPseudoColorRenderer(rasterLayer.dataProvider(), band, shader) #we have to put the band number
        rasterLayer.setRenderer(renderer)   

        #add the raster layer to the map
        QgsProject.instance().addMapLayer(rasterLayer)

        #close the netCDF file
        ncFile.close()

       
        
       
        

       
        
