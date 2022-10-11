'''
/****************************************************************************************
* 
* 
* 
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
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        #our class builds netCDF_visualization Plugins
        #self is a Plugin
        #we set the iface as an attribute!!
        self.iface = iface
        #decalre instance attributes
        self.actions = []
        self.menu = self.tr(u'&netCDFVisualizer')

    
    def tr(self, message):
        """Get the translation for a string using Qt translation API.
        We implement this ourselves since we do not inherit QObject.
        :param message: String for translation.
        :type message: str, QString
        :returns: Translated version of message.
        :rtype: QString
        """
        return QCoreApplication.translate('netCDFVisualizer', message)
        
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)
        
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        
        if add_to_toolbar:
            self.iface.addToolBarIcon(action)
        
        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)
        self.actions.append(action)
        return action

    #when we click the plugin in QGIS the plugin will be loaded
    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = ':/plugins/netCDFVisualizer/adventure.png'
        self.add_action(
            icon_path,
            text=self.tr(u'netCDFVisualizer'),
            callback=self.callMask,
            parent=self.iface.mainWindow())

    #when we close the plugin in QGIS the plugin will be unloaded
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""	
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&netCDFVisualizer'),
                action)
            self.iface.removeToolBarIcon(action)
        else :
            self.toolbar.removeAction(action)
           

    #we create a function to call the mask       
    def callMask(self):
        #we create the mask or GUI
        self.mask = maskAndFuntionality(self.iface)
        #we show the mask
        self.mask.show()

