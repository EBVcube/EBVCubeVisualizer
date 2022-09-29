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
from .netCDF_visualizer_funtionality import *

#we write a class, Plugins is a class
import os

class netCDFVisualizer:
    """This is a class for the netCDFVisualizer Plugin"""
    #we set that we need the iface to build something with the class
    def __init__(self, iface):
        #our class builds netCDF_visualization Plugins
        #self is a Plugin
        #we set the iface as an attribute!!
        self.iface = iface
        
    #when we click the plugin in QGIS the plugin will be loaded
    def initGui(self):
        #we build the menu item without placing it already in the menu
        self.pluginButton = QAction('start', self.iface.mainWindow())
        #we connect the menu item
        self.iface.addPluginToMenu('netCDFVisualizer', self.pluginButton)
        #whenever self.pluginButton is clicked, the maskCall should be executed
        self.pluginButton.triggered.connect(self.callMask)


    #when we close the plugin in QGIS the plugin will be unloaded
    def unload(self):
        #we remove the menu item
        self.iface.removePluginMenu('netCDFVisualizer', self.pluginButton)
        #we remove the menu item
        self.iface.removeToolBarIcon(self.pluginButton)   

    #we create a function to call the mask       
    def callMask(self):
        #we create the mask or GUI
        self.mask = maskAndFuntionality(self.iface)
        #we show the mask
        self.mask.show()

