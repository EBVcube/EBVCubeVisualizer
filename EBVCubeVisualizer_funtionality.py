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
from PyQt5.QtWidgets import QMessageBox
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
    """Class for the mask and the functionality of the netCDFVisualizer Plugin"""
    def __init__(self, iface):
        super(maskAndFunctionality, self).__init__(iface.mainWindow())
        self.setupUi(self)

        # Connect signals and slots
        self.btn_closePlugin.clicked.connect(self.closePlugin)
        # self.btn_inputFile.clicked.connect(self.importData)
        self.btn_remove.clicked.connect(self.removePath)
        self.btn_load.clicked.connect(self.loadNetCDF)
        self.btn_load.clicked.connect(self.setMapData)
        self.btn_remove_sel.clicked.connect(self.removeSelection)
        self.tree_data.itemClicked.connect(self.showInfo)
        self.btn_plot.clicked.connect(self.displayData)
        self.loaded_datasets = {}  # Dictionary to store dataset references with file paths as keys

    def closePlugin(self):
        """This function closes the plugin"""
        self.close()

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
        """This function removes the selection in the tree widget"""
        selected_item = self.tree_data.currentItem()

        if not selected_item:
            return

        if selected_item.parent() is None:
            dataset_name = selected_item.text(0)
            self.tree_data.takeTopLevelItem(self.tree_data.indexOfTopLevelItem(selected_item))
            self.text_info.clear()
            self.cbox_entity.clear()
            self.cbox_time.clear()
            self.cbox_scenarios.clear()
            self.cbox_metric.clear()

            # Remove from loaded datasets dictionary
            if dataset_name in self.loaded_datasets:
                self.loaded_datasets.pop(dataset_name).close()

    def loadNetCDF(self): # This function must be merge with the import data. Like this we avoid two steps to open the file
        """This function loads the netCDF file and shows the variables, groups, and sub-groups in the QTreeWidget."""
        path, _ = QFileDialog.getOpenFileName(None, "Select netCDF file", filter="*.nc")

        if not path:
            return
        
        self.text_set.setText(path)

        if path in self.loaded_datasets:
            ncFile = self.loaded_datasets[path]
        else:
            try:
                ncFile = nc.Dataset(path, 'r', format='NETCDF4')
                self.loaded_datasets[path] = ncFile  # Store the dataset in the dictionary
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to load netCDF file: {e}")
                return

        ncFileName = os.path.basename(path)
        ncFileTitle = getattr(ncFile, 'title', 'No Title')

        existing_item = self.tree_data.findItems(ncFileName, Qt.MatchExactly, 0)
        if existing_item:
            return

        top_level = QTreeWidgetItem([ncFileName, ncFileTitle])
        top_level.setData(0, Qt.UserRole, path)  # Store path for easy reference
        self.tree_data.addTopLevelItem(top_level)

        self.populateTreeWidget(ncFile, top_level)
        self.tree_data.expandAll()

        # Call setMapSata after loading the file
        self.setMapData(path)

    def populateTreeWidget(self, ncFile, parent_item):
        """Populate the tree widget with groups and variables from the NetCDF file."""
        ncFileGroupsName = list(ncFile.groups.keys())

        for group_name in ncFileGroupsName:
            longNameGroups = getattr(ncFile.groups[group_name], 'long_name', 'No Long Name')
            group_item = QTreeWidgetItem([group_name, longNameGroups])
            parent_item.addChild(group_item)

            self.addGroupVariablesAndNestedGroups(ncFile.groups[group_name], group_item)

    def addGroupVariablesAndNestedGroups(self, group, parent_item):
        """Add variables and nested groups from a given group to the tree widget."""
        variables = list(group.variables.keys())
        for var_name in variables:
            longNameVariables = getattr(group.variables[var_name], 'long_name', 'No Long Name')
            var_item = QTreeWidgetItem([var_name, longNameVariables])
            parent_item.addChild(var_item)

        nested_groups = list(group.groups.keys())
        for nested_group_name in nested_groups:
            nested_group = group.groups[nested_group_name]
            longNameGroups = getattr(nested_group, 'long_name', 'No Long Name')
            nested_group_item = QTreeWidgetItem([nested_group_name, longNameGroups])
            parent_item.addChild(nested_group_item)

            self.addGroupVariablesAndNestedGroups(nested_group, nested_group_item)

    def setMapData(self, dataset_path=None):
        """This function sets the entities, time, scenarios and metrics in the QComboBox"""
        self.cbox_entity.clear()
        self.cbox_time.clear()
        self.cbox_scenarios.clear()
        self.cbox_metric.clear()
        
        # Use the passed dataset path ot the currently loaded dataset path
        path = dataset_path if dataset_path else self.text_set.text()

        if path not in self.loaded_datasets:
            QMessageBox.warning(None, "Warning", "Please load a valid netCDF file first.")
            return

        ncFile = self.loaded_datasets[path]

        groups = list(ncFile.groups.keys()) # Get the metrics  
        groupsOfGroups = list(ncFile.groups[groups[0]].groups.keys()) if groups else [] 

        # Dictionary to map standard_name to actual group/variable names
        self.metric_name_map = {}
        self.scenario_name_map = {}

        # We populate the scenarrios drop down menu
        if groupsOfGroups:
            self.cbox_scenarios.setEnabled(True)
            self.cbox_scenarios.clear()
            
            # Add standard name to the scenarios
            for group_name in groups:
                group = ncFile.groups[group_name]
                standard_name = getattr(group, 'standard_name', group_name)
                self.cbox_scenarios.addItem(standard_name)
                self.scenario_name_map[standard_name] = group_name
        else:
            self.cbox_scenarios.addItem("no scenario")
            self.cbox_scenarios.setEnabled(False)

        # Pupulate the metrics drop down menu
        if groupsOfGroups:
            self.cbox_metric.clear()
            for sub_group_name in groupsOfGroups:
                sub_group = ncFile.groups[groups[0]].groups[sub_group_name]
                standard_name = getattr(sub_group, 'standard_name', sub_group_name)
                self.cbox_metric.addItem(standard_name)
        else:
            for group_name in groups:
                group = ncFile.groups[group_name]
                standard_name = getattr(group, 'standard_name', group_name)
                self.cbox_metric.addItem(standard_name)
                self.metric_name_map[standard_name] = group_name
                
        time = ncFile.variables['time']
        timeUnits = time.units
        timeCalendar = time.calendar
        time = nc.num2date(time[:], timeUnits, timeCalendar)
        time = [str(i).split(" ")[0] for i in time]

        self.cbox_time.clear()
        self.cbox_time.addItems(time)

        entities = ncFile.variables['entity']
        entityDrop = [np.array(entities[i]).tobytes().decode('UTF-8').strip() for i in range(len(entities))]
        self.cbox_entity.addItems(entityDrop)

    def showInfo(self):
        """Show the attributes of the scenarios, metrics, and variables."""
        self.text_info.clear()

        selected_item = self.tree_data.currentItem()
        if not selected_item:
            return

        root_item = selected_item  
        while root_item.parent():
            root_item = root_item.parent()

        dataset_path = root_item.data(0, Qt.UserRole)
        if dataset_path not in self.loaded_datasets:
            return

        ncFile = self.loaded_datasets[dataset_path]
        current_item_text = selected_item.text(0)

        if current_item_text == os.path.basename(dataset_path):
            self.displayGlobalAttributes(ncFile)
        elif current_item_text in ncFile.groups:
            self.displayGroupAttributes(ncFile.groups[current_item_text])
        elif selected_item.parent() and selected_item.parent().text(0) in ncFile.groups:
            parent_group = ncFile.groups[selected_item.parent().text(0)]
            if current_item_text in parent_group.groups:
                self.displayGroupAttributes(parent_group.groups[current_item_text])
            elif current_item_text in parent_group.variables:
                self.displayVariableAttributes(parent_group.variables[current_item_text])
        # We call setMapData to update the entities, time, scenarios and metrics in the QComboBox
        self.setMapData(dataset_path)


    def displayGlobalAttributes(self, ncFile): 
        """Display global attributes of the NetCDF file with custom formatting."""
        self.text_info.append(f"<b><font size=5>File name: {os.path.basename(ncFile.filepath())}</font></b>") # File name of the NetCDF file 
        self.text_info.append(f"<b><font size=5>Title: {ncFile.title}</font></b>") # Title of the NetCDF file
        self.text_info.append("<hr>") # 
        self.text_info.append("<b><font size=5>Global Attributes</font></b><br>") # Global Attributes 
        for attr in ncFile.ncattrs(): 
            if attr not in ['title', 'history', 'Conventions', 'date_issued']:
                self.text_info.append(f"<b><font size=4>• {attr}:</font></b> <font size=4> {ncFile.getncattr(attr)}<br>")
        # move cursor to the start of the text
        self.text_info.moveCursor(QTextCursor.Start)  # Move cursor to the top

    def displayGroupAttributes(self, group):
        """Display attributes of a NetCDF group with custom formatting."""
        groupType = "Metric" if 'metric' in group.name.lower() else "Scenario" 
        self.text_info.append(f"<b><font size=5>Attributes of the {groupType}</font></b><br>")
        self.text_info.append("<hr style='border-top: 3px double #8c8b8b;'>") 
        for attr in group.ncattrs():
            self.text_info.append(f"<b><font size=4>• {attr}:</font></b> <font size=4>{group.getncattr(attr)}<br>")
        # move cursor to the start of the text
        self.text_info.moveCursor(QTextCursor.Start)  # Move cursor to the top

    def displayVariableAttributes(self, var):
        """Display attributes of a NetCDF variable with custom formatting."""
        self.text_info.append("<b><font size=5>Attributes of the EBV cube </font></b><br>")
        self.text_info.append("<hr style='border-top: 3px double #8c8b8b;'>")

        # Exclude technical attributes
        excluded_attrs = {'grid_mapping', 'coordinates'}
        
        # Display all attributes except the excluded ones
        for attr in var.ncattrs():
            if not attr in excluded_attrs:
                self.text_info.append(f"<b><font size=4>• {attr}:</font></b> <font size=4> {var.getncattr(attr)}<br>")
        
        # move cursor to the start of the text
        self.text_info.moveCursor(QTextCursor.Start)  # Move cursor to the top

    def displayData(self):
        """This function extracts a subset of data from a NetCDF file based on the user's selections and adds it to the QGIS map as a raster layer."""
        path = self.text_set.text()
        if path not in self.loaded_datasets:
            QMessageBox.warning(None, "Warning", "Please load a valid netCDF file first.")
            return

        ncFile = self.loaded_datasets[path]

        try:
            # extract user selection from the GUI
            scenarioSelected = self.cbox_scenarios.currentText()
            metricSelected = self.cbox_metric.currentText()
            entitySelected = self.cbox_entity.currentText()
            timeSelected = self.cbox_time.currentText()

            # Retrieve the actual group/variable names using mapping dictionaries
            if self.cbox_scenarios.isEnabled():
                scenario_actual_name = self.scenario_name_map.get(scenarioSelected, scenarioSelected)
                metric_actual_name = self.metric_name_map.get(metricSelected, metricSelected)
                data_variable = ncFile.groups[scenario_actual_name].groups[metric_actual_name].variables['ebv_cube']
            else:
                metric_actual_name = self.metric_name_map.get(metricSelected, metricSelected)
                data_variable = ncFile.groups[metric_actual_name].variables['ebv_cube']

            # Retrieve entity index
            entities = ncFile.variables['entity']
            entityDrop = [np.array(entities[i]).tobytes().decode('UTF-8').strip() for i in range(len(entities))]
            entityIndex = entityDrop.index(entitySelected)

            # Retrieve time index
            time = ncFile.variables['time']
            timeUnits = time.units
            timeCalendar = time.calendar
            time = [str(i).split(" ")[0] for i in nc.num2date(time[:], timeUnits, timeCalendar)]
            timeIndex = time.index(timeSelected)
            
            # Extract the subset of data
            data_subset = data_variable[entityIndex, timeIndex, :, :]
            
            # Retrieve the standard name for the metric
            metric_standard_name = metricSelected
            if self.cbox_scenarios.isEnabled():
                metric_variable = ncFile.groups[scenario_actual_name].groups[metric_actual_name]
                metric_standard_name = metric_variable.getncattr('standard_name') if 'standard_name' in metric_variable.ncattrs() else metricSelected
            else:
                metric_variable = ncFile.groups[metric_actual_name]
                metric_standard_name = metric_variable.getncattr('standard_name') if 'standard_name' in metric_variable.ncattrs() else metricSelected

            # Retrieve the standard name for the scenario (if scenarios are enabled)
            if self.cbox_scenarios.isEnabled():
                scenario_variable = ncFile.groups[scenarioSelected]
                scenario_standard_name = scenario_variable.getncattr('standard_name') if 'standard_name' in scenario_variable.ncattrs() else scenarioSelected
            else:
                scenario_standard_name = None
            
            # Retrieve the standard name for the scenario (if scenarios are enabled)
            scenario_standard_name = None
            if self.cbox_scenarios.isEnabled():
                scenario_variable = ncFile.groups[scenario_actual_name]
                scenario_standard_name = scenario_variable.getncattr('standard_name') if 'standard_name' in scenario_variable.ncattrs() else scenarioSelected

            # Construc the layer name
            if scenario_standard_name:
                rasterName = f"{scenario_standard_name} | {metric_standard_name} | Entity: {entitySelected} | Time: {timeSelected}"
            else:
                rasterName = f"{metric_standard_name} | Entity: {entitySelected} | Time: {timeSelected}"
            

            # Create a temporary NetCDF file with the subset of data
            temp_nc_path = tempfile.mktemp(suffix='.nc')
            with nc.Dataset(temp_nc_path, 'w', format='NETCDF4') as temp_nc:
                temp_nc.createDimension('lat', len(ncFile.dimensions['lat']))
                temp_nc.createDimension('lon', len(ncFile.dimensions['lon']))
                temp_nc.createDimension('time', 1)
                temp_nc.createDimension('entity', 1)

                for dim in ['lat', 'lon']:
                    var = temp_nc.createVariable(dim, ncFile.variables[dim].datatype, (dim,))
                    var[:] = ncFile.variables[dim][:]
                    var.setncatts({k: ncFile.variables[dim].getncattr(k) for k in ncFile.variables[dim].ncattrs()})

                temp_data_var = temp_nc.createVariable('ebv_cube', data_variable.datatype, ('entity', 'time', 'lat', 'lon'))
                temp_data_var.setncatts({k: data_variable.getncattr(k) for k in data_variable.ncattrs()})
                temp_data_var[0, 0, :, :] = data_subset

            
            # Create the raster layer in QGIS
            uri = f'NETCDF:"{temp_nc_path}":ebv_cube'
            rasterLayer = QgsRasterLayer(uri, rasterName, 'gdal')

            if not rasterLayer.isValid():
                QMessageBox.warning(None, "Error", "Failed to load the raster layer.")
                return  
            
            # Get CRS from the NetCDF file
            crs_wkt = None
            if 'crs' in ncFile.variables:
                crs_var = ncFile.variables['crs']
                if 'spatial_ref' in crs_var.ncattrs():
                    crs_wkt = crs_var.getncattr('spatial_ref')
                    crs = QgsCoordinateReferenceSystem()
                    crs.createFromWkt(crs_wkt)
                    rasterLayer.setCrs(crs)

            dp = rasterLayer.dataProvider()
            band = 1
            stats = dp.bandStatistics(band)
            min_val = stats.minimumValue
            max_val = stats.maximumValue

            colorRamp = QgsColorRampShader(min_val, max_val)
            colorRamp.setColorRampType(QgsColorRampShader.Interpolated)
            colorRamp.setColorRampItemList([
                QgsColorRampShader.ColorRampItem(min_val, QColor(0, 255, 0)),
                QgsColorRampShader.ColorRampItem((min_val + max_val) / 2, QColor(255, 255, 0)),
                QgsColorRampShader.ColorRampItem(max_val, QColor(255, 0, 0))
            ])

            shader = QgsRasterShader()
            shader.setRasterShaderFunction(colorRamp)

            renderer = QgsSingleBandPseudoColorRenderer(dp, band, shader)
            rasterLayer.setRenderer(renderer)

            QgsProject.instance().addMapLayer(rasterLayer)

            QMessageBox.information(None, "Layer Added", f"The layer '{rasterName}' has been successfully added.")
        
        finally:
            pass  # Remove ncFile.close() to keep the dataset reference intact for future operations.