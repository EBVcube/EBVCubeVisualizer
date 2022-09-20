#the __init__ gives the construction order for the plugin

from .netCDF_visualization import netCDF_viewer

def classFactory(iface):
    plugin = netCDF_viewer(iface)
    return plugin





