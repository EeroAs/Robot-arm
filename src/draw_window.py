import random
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from node_graphics_item import NodeGraphicsItem
from box_graphics_item import BoxGraphicsItem
from PyQt5.QtCore import QPropertyAnimation
import box_graphics_item
from arm_object import ArmObject

class DrawWindow(QGraphicsView):
    '''
    This class is the view to the scene in which the graphical components exist and interact.
    Also methods involving these items are located here.
    '''
    
    def __init__(self, size_x, size_y):
        '''
        The self.arms contains the ArmObjects of the scene, and the self.boxes contains any added boxes
        '''
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, size_x, size_y)
        self.setScene(self.scene)
        self.width = size_x
        self.height = size_y
        self.arms = self.create_robot(100, 100, 10)
        self.boxes = []
        self.setMinimumSize(500, 500)
        self.animation_duration = 1000
        
        
    def create_robot(self,length1,length2, node_diameter):
        '''
        This function creates the robot with 2 arms, 2 nodes in-between, 
        and adds them all to the scene using PyQt, and returns the arm objects as a list for self.arms
        '''
        arm1 = ArmObject(self.width/2, self.height/2, self.width/2, self.height/2 -length1,None)
        arm2 = ArmObject(self.width/2, self.height/2-length1, self.width/2, self.height/2-length1-length2,arm1.arm)
        arm1.arm.setTransformOriginPoint(self.width/2, self.height/2)
        arm2.arm.setTransformOriginPoint(self.width/2, self.height/2 -length1)
        self.node1 = NodeGraphicsItem(self.width/2 - node_diameter/2, self.height/2-length1-node_diameter/2,node_diameter,node_diameter,arm1.arm)
        self.node2 = NodeGraphicsItem(self.width/2 - node_diameter/2, self.height/2-length1-length2-node_diameter/2,node_diameter,node_diameter,arm2.arm)
        self.scene.addItem(arm1.arm)#this will add all the created items, for they are children of arm1
        return [arm1, arm2]


    def set_animation_duration(self, duration):
        self.animation_duration = duration


    def add_box(self):
        '''
        This method will spawn a Box in a random location within the scene, and is called when the Add Box
        button is activated in the Gui
        '''
        new_box = BoxGraphicsItem()
        self.scene.addItem(new_box)
        self.boxes.append(new_box)
        new_box.setPos(random.randint(0,self.width),random.randint(0,self.height))
    
    
    def define_grab(self, checked):
        '''
        This method is called when the Grab toggle in the Gui is activated. It checks for boxes colliding with the last NodeItem,
        and calls their grab_action or let_go_action methods in accordance to the state of the grab toggle
        '''
        if checked: #grabbing
            lista = (self.node2.collidingItems())
            for i in lista:
                if isinstance(i, box_graphics_item.BoxGraphicsItem): #check that we only affect boxes
                    i.grab_action(self.node2)
                
        else: #letting go
            lista = self.node2.childItems()
            for i in lista:
                i.let_go_action(self.scene)#the scene is given as parameter to be added as the parent of the box after letting go


    def delete_all_boxes(self):
        '''
        Remove all boxes from the scene.
        '''
        for i in self.boxes:
            self.scene.removeItem(i)
        self.boxes.clear()
                    
                    
    def animate(self, value, arm_number):
        '''
        This method is called when the user hits Enter in one of the line edit fields of the Gui. It divides both arms into their
        own different animations, in order for them to be able to run simultaneously.
        '''
        arm = int(arm_number)
        if arm == 0:
            self.animate1(value)
        else:
            self.animate2(value)
      
    def animate1(self,value):
        self.animation1=QPropertyAnimation(self.arms[0], b"rot") #b"rot" is the pyqtProperty created in the ArmObject class
        self.animation1.setStartValue(self.arms[0].arm.rotation())
        self.animation1.setEndValue(float(value))
        self.animation1.setDuration(self.animation_duration)
        self.animation1.start()
        
    def animate2(self,value):
        self.animation2=QPropertyAnimation(self.arms[1], b"rot")
        self.animation2.setStartValue(self.arms[1].arm.rotation())
        self.animation2.setEndValue(float(value))
        self.animation2.setDuration(self.animation_duration)
        self.animation2.start()
        
        
    def animate_from_text(self, number_of_moves, arm1_moves, arm2_moves):
        '''
        This method is called after the Gui class is done parsing the text edit field string into commands, which it hands over to
        this method as two separate lists of moves for both arms. Two separate animations are created based on the lists in order
        to run animations simultaneously.
        '''
        if len(arm1_moves) != 0:
            self.text_animation1=QPropertyAnimation(self.arms[0], b"rot")
            self.text_animation1.setStartValue(self.arms[0].arm.rotation())
            self.text_animation1.setEndValue(arm1_moves[-1])
            self.text_animation1.setDuration(self.animation_duration*number_of_moves)
            steps1 = 1 / (len(arm1_moves)+1)
            for i in range(len(arm1_moves)-1):
                self.text_animation1.setKeyValueAt((i+1)*steps1, arm1_moves[i]) #this sets up middle values for the animation, so that each "Step" is animated
            self.text_animation1.start()
            
        if len(arm2_moves) != 0:
            self.text_animation2=QPropertyAnimation(self.arms[1], b"rot")
            self.text_animation2.setStartValue(self.arms[1].arm.rotation())
            self.text_animation2.setEndValue(arm2_moves[-1])
            self.text_animation2.setDuration(self.animation_duration*number_of_moves)
            steps2 = 1 / (len(arm2_moves)+1)
            for i in range(len(arm2_moves)-1):
                self.text_animation2.setKeyValueAt((i+1)*steps2, arm2_moves[i])
            self.text_animation2.start()
                
    