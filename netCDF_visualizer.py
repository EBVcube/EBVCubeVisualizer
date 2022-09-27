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
#we import the important functions from the pyQt5 library

from PyQt5.QtCore import *  
from PyQt5.QtGui import *  
from PyQt5.QtWidgets import *  

#import everthing from the netCDF_visualization_funtionality.py file
from netCDF_visualizer_funtionality import *

#we write a class, Plugins is a class
import os

class netCDF_visualizer:
    """This is a class for the netCDF_visualizer Plugin"""
    #we set that we need the iface to build something with the class
    def __init__(self, iface):
        #our class builds netCDF_visualization Plugins
        #self is a Plugin
        #we set the iface as an attribute!!
        self.iface = iface
        
    #when we click the plugin in QGIS the plugin will be loaded
    def initGui(self):
        #we build the menu entry without placing it in the menu
        self.pluginButton = QAction('Start', self.iface.mainWindow())
        #we add the menu entry
        self.iface.addPluginToMenu('netCDF_visualizer', self.pluginButton)
        #everytime the self.pluginButton is clicked the maskeAufrufen should be executed
        self.pluginButton.triggered.connect(self.callMask)
    
    def unload(self):
        #we have to remove the self.pluginButton and the menu entry again!1
        self.iface.removePluginMenu('netCDF_visualizer', self.pluginButton)
        
        
    def callMask (self):
        #the GUI will be built!
        self.unsereGui = maskAndFuntionality(self.iface)
        #we open the Gui
        self.unsereGui.show()

