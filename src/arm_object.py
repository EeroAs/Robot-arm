from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtCore import pyqtProperty
from PyQt5.Qt import QObject
from PyQt5.QtGui import QPen

class ArmObject(QObject):
    '''
    This class represents an arm of the robot. It inherits from QObject in order to make animations possible,
    and creates the actual arm by creating a QGraphicsLineItem, which will be added to the scene.
    '''
    
    def __init__(self,x1,y1,x2,y2,parent):
        super().__init__()
        self.arm = QGraphicsLineItem(x1,y1,x2,y2,parent)
        pen = QPen()
        pen.setWidth(3)
        self.arm.setPen(pen)
        
        
    def rotate(self,value):
        '''
        Changes the rotation to value by rotating the items local coordinate system, and 
        passing it down to its child items.
        '''
        self.arm.setRotation(float(value))
            
        
    def _set_rot(self,rot):
        "This is needed to be able to animate the arms rotation, as a property"
        self.arm.setRotation(rot)
        
    rot = pyqtProperty(float, fset=_set_rot)