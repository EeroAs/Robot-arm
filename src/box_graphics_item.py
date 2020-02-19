from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsItem
from PyQt5.Qt import QPen,QBrush,QColor,QPointF

class BoxGraphicsItem(QGraphicsRectItem):
    '''
    This class represents the boxes that the user can add to the scene, and move with the robot
    '''
    
    def __init__(self):
        super().__init__(-20,-20,40,40) #this ensures the items origin(0,0) to be in its middle
        self.setPen(QPen(QColor(0,0,0),2))
        self.setBrush(QBrush(QColor(204,0,102)))
        self.setFlag(QGraphicsItem.ItemIsMovable)#The boxes don't rotate, and are movable with the mouse
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        
        
    def grab_action(self, parent):
        '''
        This method is called when the grab button is activated with a valid box colliding with the last nodeitem.
        The parent is the last node, and by adding it as this items parent, we can move this box with it. When 
        changing the parent, this items coordinate system is also changed, so we have to update its position in the new system
        in order for the box to remain in the same absolute position
        '''
        box_scene_point = self.mapToScene(QPointF(0,0))
        parent_point = parent.mapFromScene(box_scene_point)
        self.setParentItem(parent)
        self.setPos(parent_point)
        
        
    def let_go_action(self, scene):
        "We let go by removing the parent of this item and adding this box back to the scene"
        box_scene_point = self.mapToScene(QPointF(0,0))
        self.setParentItem(None)
        scene.addItem(self)
        self.setPos(box_scene_point)