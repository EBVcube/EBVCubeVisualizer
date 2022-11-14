#the __init__ gives the construction order for the plugin
from .EBVCubeVisualizer import EBVCubeVisualizer

def classFactory(iface):
    plugin = EBVCubeVisualizer(iface)
    return plugin





