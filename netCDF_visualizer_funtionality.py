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

from tkinter import Widget
from PyQt5.Qtcore import *  
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyQt5 import uic

#we want to work with the os module
import os
#to import general tools from QGIS we need the qgis.core module
from qgis.core import *
#we want to work with the numpy module
import numpy as np
#for loading the netCDF files we need the netCDF4 module    
import netCDF4 as nc
from netCDF4 import Dataset

#we create the path to the ui file
#Path to the Ordner where the ui file is
ncPath = os.path.dirname(__file__) #the comand dirname gives the path to the directory where the file is
#path to the ui file
uiPath = os.path.join(ncPath, 'netCDF_visualizer.ui')

#two class
# WIDEGT is a class for the GUI
# BASE is a PyQt5 class to insatalize the GUI

WIDGET, BASE = uic.loadUiType(uiPath)

class maskAndFuntionality (WIDGET, BASE):
    def __init__(self, iface):
        #self = GUI/mask
        QDialog.__init__(self, iface.mainWindow())
        self.setuoUi(self)
        #self is a GUI
       
      


        
        
        




