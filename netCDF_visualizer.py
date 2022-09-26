#we import the important functions from the pyQt5 library
from PyQt5.QtCore import *  # @UnusedWildImport
from PyQt5.QtGui import *  # @UnusedWildImport
from PyQt5.QtWidgets import *  # @UnusedWildImport

#import everthing from the netCDF_visualization_funtionality.py file
from netCDF_visualization_funtionality import *

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
        self.unsereGui = maskFuntionality(self.iface)
        #we open the Gui
        self.unsereGui.show()

