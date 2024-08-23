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
# Import necessary standard libraries
import os
import tempfile
from datetime import datetime
import json

# Import PyQt5 modules for GUI development
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

# Import QGIS modules
from qgis.core import *
from qgis.utils import iface

# Import netCDF4 for handling NetCDF files
try:
    import netCDF4 as nc
except ImportError:
    raise ImportError(
        "The 'netCDF4' module is required for this plugin but is not installed. "
        "Please install it using the OSGeo4W shell or the QGIS Python console. "
        "Run `pip install netCDF4`.")

# Import additional libraries for data processing and visualization
import numpy as np
import matplotlib.pyplot as plt
from osgeo import osr, gdal, ogr


#we create the path to the ui file
#Path to the Ordner where the ui file is
ncvPath = os.path.dirname(__file__) #the comand dirname gives the path to the directory where the file is
#path to the ui file
#dosn't matter where the ui file is located in the directory 
ui_file_path = os.path.join(ncvPath, 'EBVCubeVisualizer.ui')

#TWO CLASES#    
# WIDEGT is a class for the GUI
# BASE is a PyQt5 class to insatalize the GUI
# WIDGET, BASE = uic.loadUiType(uiPath)
ui_class, base_class = uic.loadUiType(ui_file_path)

class maskAndFunctionality(base_class, ui_class):
    """Class for the mask and the funtionality of the netCDFVisualizer Plugin"""
    def __init__(self, iface):
        super(maskAndFunctionality, self).__init__(iface.mainWindow())
        self.setupUi(self)

        # Connect signals and slots
        self.btn_closePlugin.clicked.connect(self.closePlugin)
        self.btn_inputFile.clicked.connect(self.importData)
        self.btn_remove.clicked.connect(self.removePath)
        self.btn_load.clicked.connect(self.loadNetCDF)
        self.btn_load.clicked.connect(self.setMapData)
        self.btn_remove_sel.clicked.connect(self.removeSelection)
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
        # Clear the QComboBox
        self.cbox_entity.clear()
        self.cbox_time.clear()
        self.cbox_scenarios.clear()
        self.cbox_metric.clear()

        # Get the path from the text space
        path = self.text_set.text()
        ncFile = nc.Dataset(path, 'r', format='NETCDF4') 

        groups = list(ncFile.groups.keys())  # Get the metrics (name of the groups)
        groupsOfGroups = list(ncFile.groups[groups[0]].groups.keys())  # Get the scenarios (name of the groups of the groups)

        # Set scenario and metric in the QComboBox
        self.cbox_metric.addItems(groups)
        self.cbox_scenarios.addItem("not scenarios")
        self.cbox_scenarios.setEnabled(False)

        if len(groupsOfGroups) > 0:
            self.cbox_scenarios.setEnabled(True)
            self.cbox_scenarios.clear()
            self.cbox_scenarios.addItems(groups)
            self.cbox_metric.clear()
            self.cbox_metric.addItems(groupsOfGroups)
        else:
            pass

        # Get the time of the netCDF file and set it into a QComboBox
        time = ncFile.variables['time']
        timeUnits = time.units
        timeCalendar = time.calendar
        time = nc.num2date(time[:], timeUnits, timeCalendar)
        time = [str(i).split(" ")[0] for i in time]  # Leave just the date and not the time

        self.cbox_time.clear()
        self.cbox_time.addItems(time)

        # Get the entities
        self.cbox_entity.clear()
        entities = ncFile.variables['entity']

        entityDrop = []
        for i in range(len(entities)):
            entity = np.array(entities[i])
            entity = entity.tobytes().decode('UTF-8').strip()  # Use tobytes instead of tostring
            entityDrop.append(entity)

        self.cbox_entity.addItems(entityDrop)
        ncFile.close()
    
    
    # def setMapData(self):
        # """This function sets the entities, time, scenarios and metrics in the QComboBox"""
        # #we clear the QComboBox
        # self.cbox_entity.clear()
        # self.cbox_time.clear()
        # self.cbox_scenarios.clear()
        # self.cbox_metric.clear()
        
        # #we get the path from the text space
        # path = self.text_set.text()
        # ncFile = nc.Dataset(path, 'r', format='NETCDF4') 

        # groups = list(ncFile.groups.keys()) #we get the metrics (name of the groups)
        # groupsOfGroups = list(ncFile.groups[groups[0]].groups.keys()) #we get the scenarios(name of the groups of the groups)


        # #set scenario and metric in the QComboBox  
        # #if there is just groups we set the groups in the cbox_metric 
        # self.cbox_metric.addItems(groups)
        # self.cbox_scenarios.addItem("not scenarios")
        # self.cbox_scenarios.setEnabled(False)
        
        # if len(groupsOfGroups)>0:
            # self.cbox_scenarios.setEnabled(True)
            # self.cbox_scenarios.clear()
            # self.cbox_scenarios.addItems(groups)
            # self.cbox_metric.clear()
            # self.cbox_metric.addItems(groupsOfGroups)
        # else:
            # pass

        # #here we are gonna get the entities and the time of the netCDF file and set them into a QComboBox if the top level is clicked
        # #we get the time of the netCDF file
        # time = ncFile.variables['time']
        # timeUnits = time.units
        # timeCalendar = time.calendar
        # time = nc.num2date(time[:], timeUnits, timeCalendar)
        # time = [str(i).split(" ")[0] for i in time] #we leave just the date and not the time

        # #we set the time into the QComboBox
        # self.cbox_time.clear()
        # self.cbox_time.addItems(time)
        
     
        # #we get the entities
        # self.cbox_entity.clear()
        # entities = ncFile.variables['entity']
        
        # #empty list
        # entityDrop = []
        
        # for i in range(len(entities)):
            # entity = entities[i]
            # entity = np.array(entity)
            # entity = entity.tostring().decode('UTF-8').strip()
            # #print(entity)
            # #print(type(entity))
            # entityDrop.append(entity)

        # #set the entities inyo the cbox_enity
        # self.cbox_entity.addItems(entityDrop)
        
        # #check the number of entitites
        # #entityNumber = len(entityDrop)
        # #print(entityNumber)

        # #we close the netCDF file
        # ncFile.close()
    
    def showInfo(self):
        """Show the attributes of the scenarios, metrics, and variables."""
        self.text_info.clear()
        path = self.text_set.text()
        ncFile = nc.Dataset(path, 'r', format='NETCDF4')
        ncFileName = os.path.basename(path)
        ncFileTitle = ncFile.title
        globalAttributesName = list(ncFile.ncattrs())
        globalAttributesName = [attr for attr in globalAttributesName if attr not in ['title', 'history', 'Conventions', 'date_issued']]

        scenarioOrMetric = list(ncFile.groups.keys())
        metrics = [list(ncFile.groups[grp].groups.keys()) for grp in scenarioOrMetric]
        metricsVariables1 = [list(ncFile.groups[grp].variables.keys()) for grp in scenarioOrMetric]
        metricsVariables2 = [[list(ncFile.groups[grp].groups[subgrp].variables.keys()) for subgrp in metrics[0]] for grp in scenarioOrMetric]

        current_item = self.tree_data.currentItem().text(0)

        if current_item == ncFileName:
            self.text_info.append(f"<b><font size=4>File name: {ncFileName}</font></b>")
            self.text_info.append(f"<b><font size=4>Title: {ncFileTitle}</font></b>")
            self.text_info.append("<hr>")
            self.text_info.append("<b><font size=4>Global attributes: </font></b>")
            self.text_info.append("<br>")
            for attr in globalAttributesName:
                self.text_info.append(f"<b><font size=3>- {attr}: </font></b>{ncFile.getncattr(attr)}<br>")

        elif current_item in scenarioOrMetric:
            groupName = current_item
            groupStandardName = ncFile.groups[groupName].getncattr('standard_name')
            self.text_info.append(f"<b><font size=4>File name: {ncFileName}</font></b>")
            self.text_info.append(f"<b><font size=4>Title: {ncFileTitle}</font></b>")
            self.text_info.append("<hr>")

            # Determine if this is a scenario or a metric
            if groupName.startswith('scenario'):
                self.text_info.append(f"<b><font size=4>Attributes of the Scenario: </font></b>{groupStandardName}")
            else:
                self.text_info.append(f"<b><font size=4>Attributes of the Metric: </font></b>{groupStandardName}")
            self.text_info.append("<br>")

            groupAttributesName = list(ncFile.groups[groupName].ncattrs())
            groupAttributesName.remove('standard_name')
            for attr in groupAttributesName:
                self.text_info.append(f"<b><font size=3>- {attr}: </font></b>{ncFile.groups[groupName].getncattr(attr)}<br>")

        elif current_item in metrics[0]:
            scenarioName = self.tree_data.currentItem().parent().text(0)
            scenarioStandardName = ncFile.groups[scenarioName].getncattr('standard_name')
            self.text_info.append(f"<b><font size=4>File name: {ncFileName}</font></b>")
            self.text_info.append(f"<b><font size=4>Title: {ncFileTitle}</font></b>")
            self.text_info.append("<hr>")
            self.text_info.append(f"<b><font size=4>Attributes of the Scenario: </font></b>{scenarioStandardName}<br>")
            attributesNameScenario = list(ncFile.groups[scenarioName].ncattrs())
            attributesNameScenario.remove('standard_name')
            for attr in attributesNameScenario:
                self.text_info.append(f"<b><font size=3>- {attr}: </font></b>{ncFile.groups[scenarioName].getncattr(attr)}<br>")
            self.text_info.append("<hr>")

            metricName = self.tree_data.currentItem().text(0)
            metricStandardName = ncFile.groups[scenarioName].groups[metricName].getncattr('standard_name')
            self.text_info.append(f"<b><font size=4>Attributes of the Metric: </font></b>{metricStandardName}<br>")
            attributesNameMetric = list(ncFile.groups[scenarioName].groups[metricName].ncattrs())
            if 'standard_name' in attributesNameMetric:
                attributesNameMetric.remove('standard_name')
            for attr in attributesNameMetric:
                self.text_info.append(f"<b><font size=3>- {attr}: </font></b>{ncFile.groups[scenarioName].groups[metricName].getncattr(attr)}<br>")

            variableName = self.tree_data.currentItem().text(0)
            attributesNameCube = list(ncFile.groups[scenarioName].groups[metricName].variables[variableName].ncattrs())
            for attribute in ['_FillValue', 'grid_mapping', 'coordinate']:
                if attribute in attributesNameCube:
                    attributesNameCube.remove(attribute)
            for attr in attributesNameCube:
                self.text_info.append(f"<b><font size=3>- {attr}: </font></b>{ncFile.groups[scenarioName].groups[metricName].variables[variableName].getncattr(attr)}<br>")
            fillValue = ncFile.groups[scenarioName].groups[metricName].variables[variableName].getncattr('_FillValue')
            self.text_info.append(f"<b><font size=3>- Nodata_value: </font></b>{fillValue}<br>")

        elif len(metricsVariables2[0]) != 0 and current_item in metricsVariables2[0][0]:
            scenarioName = self.tree_data.currentItem().parent().parent().text(0)
            scenarioStandardName = ncFile.groups[scenarioName].getncattr('standard_name')
            self.text_info.append(f"<b><font size=4>File name: {ncFileName}</font></b>")
            self.text_info.append(f"<b><font size=4>Title: {ncFileTitle}</font></b>")
            self.text_info.append("<hr>")
            self.text_info.append(f"<b><font size=4>Attributes of the Scenario: </font></b>{scenarioStandardName}<br>")
            attributesNameScenario = list(ncFile.groups[scenarioName].ncattrs())
            attributesNameScenario.remove('standard_name')
            for attr in attributesNameScenario:
                self.text_info.append(f"<b><font size=3>- {attr}: </font></b>{ncFile.groups[scenarioName].getncattr(attr)}<br>")
            self.text_info.append("<hr>")

            metricName = self.tree_data.currentItem().parent().text(0)
            metricStandardName = ncFile.groups[scenarioName].groups[metricName].getncattr('standard_name')
            self.text_info.append(f"<b><font size=4>Attribuites of the Metric: </font></b>{metricStandardName}<br>")
            attributesNameMetric = list(ncFile.groups[scenarioName].groups[metricName].ncattrs())
            attributesNameMetric.remove('standard_name')
            for attr in attributesNameMetric:
                self.text_info.append(f"<b><font size=3>- {attr}: </font></b>{ncFile.groups[scenarioName].groups[metricName].getncattr(attr)}<br>")
            self.text_info.append("<hr>")

            variableName = self.tree_data.currentItem().text(0)
            attributesNameCube = list(ncFile.groups[scenarioName].groups[metricName].variables[variableName].ncattrs())
            for attribute in ['_FillValue', 'grid_mapping', 'coordinate']:
                if attribute in attributesNameCube:
                    attributesNameCube.remove(attribute)
            for attr in attributesNameCube:
                self.text_info.append(f"<b><font size=3>- {attr}: </font></b>{ncFile.groups[scenarioName].groups[metricName].variables[variableName].getncattr(attr)}<br>")
            fillValue = ncFile.groups[scenarioName].groups[metricName].variables[variableName].getncattr('_FillValue')
            self.text_info.append(f"<b><font size=3>- Nodata_value: </font></b>{fillValue}<br>")

        elif current_item == metricsVariables1[0][0]:
            metricName = self.tree_data.currentItem().parent().text(0)
            standardMetricName = ncFile.groups[metricName].getncattr('standard_name')
            self.text_info.append(f"<b><font size=4>File name: {ncFileName}</font></b>")
            self.text_info.append(f"<b><font size=4>Title: {ncFileTitle}</font></b>")
            self.text_info.append("<hr>")
            self.text_info.append(f"<b><font size=4>Attributes of Metric: </font></b>{standardMetricName}<br>")
            attributesNameMetric = list(ncFile.groups[metricName].ncattrs())
            attributesNameMetric.remove('standard_name')
            for attr in attributesNameMetric:
                self.text_info.append(f"<b><font size=3>- {attr}: </font></b>{ncFile.groups[metricName].getncattr(attr)}<br>")
            self.text_info.append("<hr>")

            variableName = self.tree_data.currentItem().text(0)
            attributesNameCube = list(ncFile.groups[metricName].variables[variableName].ncattrs())
            for attribute in ['_FillValue', 'grid_mapping', 'coordinate']:
                if attribute in attributesNameCube:
                    attributesNameCube.remove(attribute)
            for attr in attributesNameCube:
                self.text_info.append(f"<b><font size=3>- {attr}: </font></b>{ncFile.groups[metricName].variables[variableName].getncattr(attr)}<br>")
            fillValue = ncFile.groups[metricName].variables[variableName].getncattr('_FillValue')
            self.text_info.append(f"<b><font size=3>- nodata_value: </font></b>{fillValue}<br>")
        ncFile.close()
        
    
    # def showInfo(self):
        # """show the attributes of the scenarios, metrics and variables"""
        # self.text_info.clear()
        # path = self.text_set.text() #we get the path from the text space
        # ncFile = nc.Dataset(path, 'r', format='NETCDF4') #we open the netCDF file
        # ncFileName = os.path.basename(path) 
        # ncFileTitle = ncFile.title 
        # globalAttributesName = list(ncFile.ncattrs())
        # print(self.tree_data.currentItem().text(0))
        
        # # Remove non-essential global attributes from the list
        # for attr in ['title', 'history', 'Conventions', 'date_issued']:
            # if attr in globalAttributesName:
                # globalAttributesName.remove
        
        # # # here remove the info and add the attributes of the selected variable
        # # globalAttributesName.remove('title')
        # # globalAttributesName.remove('history')
        # # globalAttributesName.remove('Conventions')
        # # globalAttributesName.remove('date_issued')
        

        # #groups could be scenarios or metrics
        # scenarioOrMetric = list(ncFile.groups.keys())
        
        # #first group is scenarios we get the metrics
        # metrics = []
        # for i in range(len(scenarioOrMetric)):
            # metrics.append(list(ncFile.groups[scenarioOrMetric[i]].groups.keys()))

        # #first group is metric we get the variables
        # metricsVariables1 = [] 
        # for i in range(len(scenarioOrMetric)):
            # variables = list(ncFile.groups[scenarioOrMetric[i]].variables.keys())
            # metricsVariables1.append(variables)
        
        # #first group is scenario and second metric than we get the variables of metric
        # metricsVariables2 = []
        # for i in range(len(scenarioOrMetric)):
            # metricsVariables2.append([])
            # for j in range(len(metrics[i])):
                # variables = list(ncFile.groups[scenarioOrMetric[i]].groups[metrics[i][j]].variables.keys())
                # metricsVariables2[i].append(variables)

        
        # #we print everthing
        # # print('ScenarioOrMetric')
        # # print(scenarioOrMetric)
        # # print(metricsVariables1)
        # # print('metrics')
        # # print(metrics)
        # # print(metricsVariables2)
        # # print('len')
        # # print(len(metricsVariables2))
        # # print(len(metricsVariables2[0]))
        # # #print('metricsVariables1[0]')
        # # #print(metricsVariables1[0][0])
        # # print('current item')
        # # print(self.tree_data.currentItem().text(0))
        
        # current_item = self.tree_data.currentItem().text(0)
        
        # #set global attributes from the netCDF file
        # if  current_item == ncFileName:
            # #print('global atts')
            # self.text_info.clear()
            # self.text_info.append(f"<b><font size=4>File name: {ncFileName}</font></b>")
            # self.text_info.append(f"<b><font size=4>Title: {ncFileTitle}</font></b>")
            # self.text_info.append("____________________________________________________________________________")
            # self.text_info.append(" ")
            # self.text_info.append("<b><font size=4>Global attributes: </font></b>")
            # self.text_info.append(" ")
            # for attr in globalAttributesName:
                # self.text_info.append(f"<b><font size=3>- {attr}: </font></b>{ncFile.getncattr(attr)}")

        # #attributes of the groups. The groups are scenarios or metrics
        # elif currentItem in scenarioOrMetric:
            # groupName = current_item
            # groupStandardName = ncFile.groups[groupName].getncattr('standard_name')
            # self.text_info.append("<b><font size=4>" + "File name: " + ncFileName + "</font></b>")
            # self.text_info.append("<b><font size=4>" + "Title: " + ncFileTitle + "</font></b>")
            # self.text_info.append("________________________________________________________________________________")
            # self.text_info.append(" ")

            # #Scenario or Metric
            # #name and standard name of the groups (scenarios or metrics)
            # groupName = self.tree_data.currentItem().text(0)
            # #print ('scenarioName' + groupName)
            # groupStandardName = ncFile.groups[groupName].getncattr('standard_name')
            # #print ('scenarioStandardName: ' + groupStandardName)

            # #attributes of the groups (scenarios or metrics)
            # self.text_info.append("<b><font size=4>" + "Attributes of the Scenario: " + "</font></b>" + groupStandardName)
            # self.text_info.append(" ")

            # #name attributes of the groups (scenarios or metrics)
            # groupAttributesName = list(ncFile.groups[groupName].ncattrs())
            # groupAttributesName.remove('standard_name')
            # #print ('groupAttributesName: ' + str(groupAttributesName))

            # #value of the attributes of the groups
            # for i in range(len(groupAttributesName)):
                # groupAttributes = ncFile.groups[groupName].getncattr(groupAttributesName[i])
                # #print ('groupAttributes: ' + str(groupAttributes))
                # self.text_info.append("<b><font size=3>" + "-" + groupAttributesName[i] + ": " + "</font></b>" + str(groupAttributes))
            
        
        # #groups of the scenarios are always metric
        # elif self.tree_data.currentItem().text(0) in metrics[0]:
            # #print('test metric')
            # self.text_info.clear()
            # self.text_info.append("<b><font size=4>" + "File name: " + ncFileName + "</font></b>")
            # self.text_info.append("<b><font size=4>" + "Title: " + ncFileTitle + "</font></b>")
            # self.text_info.append("________________________________________________________________________________")
            # self.text_info.append(" ")

            # #Scenarios
            # #get the standard name of the scenario
            # scenarioName = self.tree_data.currentItem().parent().text(0)
            # #print ("standard name: " + scenarioName)            
            # scenarioStandardName = ncFile.groups[scenarioName].getncattr('standard_name')
            # #print ("scenario standard name: " + scenarioStandardName)
            
            # #attributes of the scenario
            # self.text_info.append("<b><font size=4>" + "Attributes of the Scenario: " + "</font></b>" + scenarioStandardName)
            # self.text_info.append(" ")
            
            # #name of the attributes of the scenario
            # attributesNameScenario = ncFile.groups[scenarioName].ncattrs()
            # attributesNameScenario.remove('standard_name')
            # #print ("attributes name: " + str(attributesNameScenario))

            # #value of the attributes of the scenario
            # for i in range(len( attributesNameScenario)):
                # attributes = ncFile.groups[scenarioName].getncattr(attributesNameScenario[i])
                # self.text_info.append("<b><font size=3>" + "-" + attributesNameScenario[i] + ": " + "</font></b>" + str(attributes))
            # self.text_info.append("________________________________________________________________________________")
            # self.text_info.append(" ")
            
            # #Metrics
            # #get name and standard name of the metric
            # metricName = self.tree_data.currentItem().text(0)
            # print ("metric name: " + metricName)
            # metricStandardName = ncFile.groups[scenarioName].groups[metricName].getncattr('standard_name')
            # print ("metric standard name: " + metricStandardName)
    
            # self.text_info.append("<b><font size=4>" + "Attributes of the Metric: " + "</font></b>" + metricStandardName)
            # self.text_info.append(" ")
            
            # #get the name of the attributes of the metric
            # attributesNameMetric = ncFile.groups[scenarioName].groups[metricName].ncattrs()
            # print ("attributes name metric: " + str(attributesNameMetric))
            # #attributesNameMetric.remove('standard_name')
            
            # for i in range(len(attributesNameMetric)):
                # attributes = ncFile.groups[scenarioName].groups[metricName].getncattr(attributesNameMetric[i])
                # print ("attributes: " + str(attributes))
                # self.text_info.append("<b><font size=3>" + "-" + attributesNameMetric[i] + ": " + "</font></b>" + str(attributes))
            
        
        # #varibles of the metric, when there is scenarios
        # elif len(metricsVariables2[0])!= 0 :
            # if self.tree_data.currentItem().text(0) in metricsVariables2[0][0]:
                # #print('test')
                # self.text_info.clear()
                # self.text_info.append("<b><font size=4>" + "File name: " + ncFileName + "</font></b>")
                # self.text_info.append("<b><font size=4>" + "Title: " + ncFileTitle + "</font></b>")
                # self.text_info.append("________________________________________________________________________________")
                # self.text_info.append(" ")
                
                # #Scenario
                # #get the name of the scenario and 
                # scenarioName = self.tree_data.currentItem().parent().parent().text(0)
                # #print('scenario Name: ' + str(scenarioName))
                # scenarioStandardName = ncFile.groups[scenarioName].getncattr('standard_name')
                # #print('scenario Standard Name: ' + str(scenarioStandardName))
                
                # #attributes of the scenario
                # self.text_info.append("<b><font size=4>" + "Attributes of the Scenario: " + "</font></b>" + scenarioStandardName)
                # self.text_info.append(" ")

                # #get the name of the attributes of the scenario
                # attributesNameScenario = ncFile.groups[scenarioName].ncattrs()
                # attributesNameScenario.remove('standard_name')
                # #print(attributesNameScenario)
                
                # #get the value of the attributes of the scenario
                # for i in range(len(attributesNameScenario)):
                    # attributesScenario = ncFile.groups[scenarioName].getncattr(attributesNameScenario[i])
                    # #print(attributesScenario)
                    # self.text_info.append("<b><font size=3>" + "-" + attributesNameScenario[i] + ": " + "</font></b>" + str(attributesScenario))
                # self.text_info.append("________________________________________________________________________________")
                # self.text_info.append(" ")
                
                # #Metric
                # #get the name of the metric
                # metricName = self.tree_data.currentItem().parent().text(0)
                # #print('metric Name: ', metricName)
                # metricStandardName = ncFile.groups[scenarioName].groups[metricName].getncattr('standard_name')
                # #print('metric standard name: ', metricStandardName)
                
                # #attributes of the metric
                # self.text_info.append("<b><font size=4>" + "Attribuites of the Metric: " + "</font></b>" + metricStandardName) 
                # self.text_info.append(" ")

                # #get the name of the attributes of the metric
                # attributesNameMetric = ncFile.groups[scenarioName].groups[metricName].ncattrs()
                # attributesNameMetric.remove('standard_name')
                # #print('Attributes name metric: ', attributesNameMetric)
      
                # #get the value of the attributes of the metric
                # for i in range(len(attributesNameMetric)):
                    # attributesMetric = ncFile.groups[scenarioName].groups[metricName].getncattr(attributesNameMetric[i])
                    # #print ('Attributes metric: ', attributesMetric)
                    # self.text_info.append("<b><font size=3>" + "-" + attributesNameMetric[i] + ": " + "</font></b>" + str(attributesMetric))
                # self.text_info.append("___________________________________________________________________________")
                # self.text_info.append(" ")
                
                # #EBV Cube
                # #attributes of the EBV Cube
                # self.text_info.append("<b><font size=4>" + "Attributes of the EBV Cube:" + "</font></b>")
                # self.text_info.append(" ")
                
                # #get the name of the attributes of the EBV Cube
                # variableName = self.tree_data.currentItem().text(0)
                # #print(variableName)
                # attributesNameCube = ncFile.groups[scenarioName].groups[metricName].variables[variableName].ncattrs()
                # attributesNameCube.remove('_FillValue')
                # attributesNameCube.remove('grid_mapping')
                # attributesNameCube.remove('coordinate')
                # #print('attributes name EBV Cube: ', attributesNameCube)
                
                # #get the value of the attributes of the EBV Cube
                # for i in range(len(attributesNameCube)):
                    # attributesCube = ncFile.groups[scenarioName].groups[metricName].variables[variableName].getncattr(attributesNameCube[i])
                    # #print('attributes cube: ', attributesCube)
                    # self.text_info.append("<b><font size=3>" + "-" + attributesNameCube[i] + ": " + "</font></b>" + str(attributesCube))
    
                # #we get the _FillValue
                # fillValue = ncFile.groups[scenarioName].groups[metricName].variables[variableName].getncattr('_FillValue')
                # #print('fill value: ', fillValue)
                # self.text_info.append("<b><font size=3>" + "-" + "Nodata_value: " + "</font></b>" + str(fillValue))
                


        # #if the groups are just metrics we get the variables of the metrics
        # elif self.tree_data.currentItem().text(0) == metricsVariables1[0][0]:
            # #print('ebv cube when ther is just metric')
            # self.text_info.clear()
            # self.text_info.append("<b><font size=4>" + "File name: " + ncFileName + "</font></b>")
            # self.text_info.append("<b><font size=4>" + "Title: " + ncFileTitle + "</font></b>")
            # self.text_info.append("___________________________________________________________________________")
            # self.text_info.append(" ")

            # #Metric
            # #name of the metrics and the standard name
            # metricName = self.tree_data.currentItem().parent().text(0)
            # #print('metric name: ' + metricName)
            # standardMetricName = ncFile.groups[metricName].getncattr('standard_name')
            # #print('standard Metric Name: ' + standardMetricName)
            
            # #attributes of the metric
            # self.text_info.append("<b><font size=4>" + "Attributes of Metric: " + "</font></b>" + standardMetricName )
            # self.text_info.append(" ")

            # #name of the attributes of the metric
            # attributesNameMetric = ncFile.groups[metricName].ncattrs()
            # #print('attributesNameCube: ', attributesNameMetric)
            # attributesNameMetric.remove('standard_name')
            
            # for i in range(len(attributesNameMetric)):
                # attributesMetric = ncFile.groups[metricName].getncattr(attributesNameMetric[i])
                # self.text_info.append("<b><font size=3>" + "-" + attributesNameMetric[i] + ": " + "</font></b>" + str(attributesMetric))
            # self.text_info.append("___________________________________________________________________________")
            # self.text_info.append(" ")

            # #EBV Cube
            # #Attributes of the EBV Cube
            # self.text_info.append("<b><font size=4>" + "Attributes of the EBV Cube: " + "</font></b>")
            # self.text_info.append(" ")

            # #name of the EBV Cube
            # cubeName = self.tree_data.currentItem().text(0)
            # #print('variable name: ' + cubeName)
            # attributesNameCube = ncFile.groups[metricName].variables[cubeName].ncattrs()
            # attributesNameCube.remove('_FillValue')
            # attributesNameCube.remove('grid_mapping')
            # attributesNameCube.remove('coordinate')
            # #print('attributesNameCube: ', attributesNameCube)

            # #get the value of the attributes of the EBV Cube
            # for i in range(len(attributesNameCube)):
                # attributesCube = ncFile.groups[metricName].variables[cubeName].getncattr(attributesNameCube[i])
                # #print ('attributesCube: ' + attributesCube)
                # self.text_info.append("<b><font size=3>" + "-" + attributesNameCube[i] + ": " + "</font></b>" + str(attributesCube))

            # #set NoData_value
            # fillValue = ncFile.groups[metricName].variables[cubeName].getncattr('_FillValue')
            # #print ('fillValue: ', fillValue)
            # self.text_info.append("<b><font size=3>" + "-" + "nodata_value: " + "</font></b>" + str(fillValue))
            # #print ('Eres la mera verga!! sigue asi. Todo sladrá bien en el futuro')
        
        # # we close the netCDF file
        # ncFile.close()


    def displayData(self):
        """This function extracts a subset of data from a NetCDF file based on the user's selections and adds it to the QGIS map as a raster layer."""
        
        # Get the path from the text field
        path = self.text_set.text()
        ncFile = nc.Dataset(path, 'r', format='NETCDF4')

        try:
            # Debug: Print the structure of the NetCDF file
            print("NetCDF file structure:")
            print(ncFile)

            # Navigate to the correct group based on scenario and metric
            if self.cbox_scenarios.isEnabled():
                scenarioSelected = self.cbox_scenarios.currentText()
                metricSelected = self.cbox_metric.currentText()
                if scenarioSelected in ncFile.groups:
                    if metricSelected in ncFile.groups[scenarioSelected].groups:
                        data_variable = ncFile.groups[scenarioSelected].groups[metricSelected].variables['ebv_cube']
                    else:
                        print(f"Metric '{metricSelected}' not found in scenario '{scenarioSelected}'.")
                        return
                else:
                    print(f"Scenario '{scenarioSelected}' not found.")
                    return
            else:
                metricSelected = self.cbox_metric.currentText()
                if metricSelected in ncFile.groups:
                    data_variable = ncFile.groups[metricSelected].variables['ebv_cube']
                else:
                    print(f"Metric '{metricSelected}' not found.")
                    return
            
            # Handle entity selection (since entities are the first dimension)
            entities = ncFile.variables['entity']
            entityDrop = [np.array(entities[i]).tobytes().decode('UTF-8').strip() for i in range(len(entities))]
            entitySelected = self.cbox_entity.currentText()
            entityIndex = entityDrop.index(entitySelected)

            # Handle time selection (since time is the second dimension)
            time = ncFile.variables['time']
            timeUnits = time.units
            timeCalendar = time.calendar
            time = [str(i).split(" ")[0] for i in nc.num2date(time[:], timeUnits, timeCalendar)]
            timeSelected = self.cbox_time.currentText()
            timeIndex = time.index(timeSelected)

            # Debug: Print selected indices and data shape
            #print(f"Selected Entity Index: {entityIndex}, Time Index: {timeIndex}")
            #print(f"Shape of data variable: {ncFile.variables['ebv_cube'].shape}")

            # Get selected scenario and metric
            scenarioSelected = self.cbox_scenarios.currentText()
            metricSelected = self.cbox_metric.currentText()

            # Subset the data based on the selections
            if self.cbox_scenarios.isEnabled():
                data_variable = ncFile.groups[scenarioSelected].groups[metricSelected].variables['ebv_cube']
            else:
                data_variable = ncFile.groups[metricSelected].variables['ebv_cube']

            # Ensure the indices are within the bounds of the data variable
            if entityIndex >= data_variable.shape[0] or timeIndex >= data_variable.shape[1]:
                print(f"Indices out of bounds: entityIndex={entityIndex}, timeIndex={timeIndex}")
                return

            # Extract the subset (note that entity is first, time is second)
            data_subset = data_variable[entityIndex, timeIndex, :, :]

             # Retrieve the CRS information from the 'crs' variable
            crs_wkt = None
            if 'crs' in ncFile.variables:
                crs_var = ncFile.variables['crs']
                if 'spatial_ref' in crs_var.ncattrs():
                    crs_wkt = crs_var.getncattr('spatial_ref')



            # Create a temporary NetCDF file to store the subset
            temp_nc_path = tempfile.mktemp(suffix='.nc')
            with nc.Dataset(temp_nc_path, 'w', format='NETCDF4') as temp_nc:
                # Copy the relevant dimensions
                temp_nc.createDimension('lat', len(ncFile.dimensions['lat']))
                temp_nc.createDimension('lon', len(ncFile.dimensions['lon']))
                temp_nc.createDimension('time', 1)  # Only one time step
                temp_nc.createDimension('entity', 1)  # Only one entity

                # Copy coordinate variables
                for dim in ['lat', 'lon']:
                    var = temp_nc.createVariable(dim, ncFile.variables[dim].datatype, (dim,))
                    var[:] = ncFile.variables[dim][:]
                    var.setncatts({k: ncFile.variables[dim].getncattr(k) for k in ncFile.variables[dim].ncattrs()})
                
                # Create the data variable with the subset
                temp_data_var = temp_nc.createVariable('ebv_cube', data_variable.datatype, ('entity', 'time', 'lat', 'lon'))
                temp_data_var.setncatts({k: data_variable.getncattr(k) for k in data_variable.ncattrs()})
                temp_data_var[0, 0, :, :] = data_subset

            # Load the temporary NetCDF file into QGIS
            uri = f'NETCDF:"{temp_nc_path}":ebv_cube'
            rasterName = f"{metricSelected}_entity: {entitySelected}_time: {timeSelected}"
            rasterLayer = QgsRasterLayer(uri, rasterName)

            # Check if the layer is valid
            if not rasterLayer.isValid():
                print("Failed to load the raster layer.")
                return
            
            # Set the CRS of the raster layer
            if crs_wkt:
                crs = QgsCoordinateReferenceSystem()
                crs.createFromWkt(crs_wkt)
                rasterLayer.setCrs(crs)

            # Set custom band naem
            dp = rasterLayer.dataProvider()
            band = 1
    
            # Build the color ramp and renderer
            stats = dp.bandStatistics(band)  # Only one band in the subset
            min_val = stats.minimumValue
            max_val = stats.maximumValue

            # Build the color ramp and renderer
            colorRamp = QgsColorRampShader(min_val, max_val)
            colorRamp.setColorRampType(QgsColorRampShader.Interpolated)

            # Define custom colors (replace with your desired colors)
            colorRamp.setColorRampItemList([
                QgsColorRampShader.ColorRampItem(min_val, QColor(0, 255, 0)),  # Green for minimum value
                QgsColorRampShader.ColorRampItem((min_val + max_val) / 2, QColor(255, 255, 0)),  # Yellow for mid-range value
                QgsColorRampShader.ColorRampItem(max_val, QColor(255, 0, 0))  # Red for maximum value
            ])
            
            shader = QgsRasterShader()
            shader.setRasterShaderFunction(colorRamp)
            
            renderer = QgsSingleBandPseudoColorRenderer(dp,band,shader)
            rasterLayer.setRenderer(renderer)
            
            # Add the raster layer to the map
            QgsProject.instance().addMapLayer(rasterLayer)

        finally:
            # Ensure the NetCDF file is closed
            ncFile.close()