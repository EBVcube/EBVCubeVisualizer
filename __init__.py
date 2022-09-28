#the __init__ gives the construction order for the plugin
from netCDFVisualizer.netCDF_visualizer import netCDFVisualizer

def classFactory(iface):
    plugin = netCDFVisualizer(iface)
    return plugin





