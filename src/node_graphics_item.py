from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtGui import QBrush,QColor

class NodeGraphicsItem(QGraphicsEllipseItem):
    '''
    This class represents the joints of the robot, and are chained to the positions of the arms
    '''

    def __init__(self, x, y, width, height, parent):
        '''
        Parent is the ArmGraphicsItem, in which the node is to be attached.
        '''
        super().__init__(x,y,width,height,parent)
        self.setBrush(QBrush(QColor(255,0,0)))
        
