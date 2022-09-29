#the __init__ gives the construction order for the plugin
from .netCDF_visualizer import netCDFVisualizer

def classFactory(iface):
    plugin = netCDFVisualizer(iface)
    return plugin





