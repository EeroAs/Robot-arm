from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QTextEdit, QCheckBox, QLabel, QPushButton, QGridLayout, QShortcut, QMessageBox)
from PyQt5.Qt import Qt, QIcon
from PyQt5.QtGui import QDoubleValidator, QKeySequence, QPixmap
from draw_window import DrawWindow

class Gui(QWidget):
    '''
    This class is a single widget that forms all the sub-widgets and handles their placement and values.
    This widget is then added as the central widget to the main_window of the program.
    '''
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.connect_signals()
        
        
    def init_ui(self):
        '''
        This initiates the actual widgets and adds them to a grid layout
        '''
        #create needed widgets
        self.slider1 = QSlider(Qt.Horizontal)
        self.slider2 = QSlider(Qt.Horizontal)
        self.line_e1 = QLineEdit()
        self.line_e2 = QLineEdit()
        self.add_box_btn = QPushButton("Add box")
        self.grab_btn = QCheckBox("Grab")
        self.text_edit = QTextEdit()
        self.view = DrawWindow(600,600)#the graphics view
        self.l1 = QLabel("Arm 1 Controls:")
        self.l2 = QLabel("Arm 2 Controls:")
        self.l3 = QLabel("-Press the 'Add box' button to spawn a box into the field\n\n"
                         "-Click the Grab option to grab onto a box with the end\n"
                         "of the arm, and click again to let go\n\n"
                         "-You can move boxes with the mouse, and pressing 'Del'\n"
                         "will remove all boxes from the field")
        
        #add widgets to gridlayout
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.l1,0,0)
        grid.addWidget(self.l2,1,0)
        grid.addWidget(self.l3,3,1,Qt.AlignTop)
        grid.addWidget(self.slider1,0,1)
        grid.addWidget(self.slider2,1,1)
        grid.addWidget(self.add_box_btn,2,0)
        grid.addWidget(self.text_edit,3,0)
        grid.addWidget(self.line_e1,0,2)
        grid.addWidget(self.line_e2,1,2)
        grid.addWidget(self.grab_btn,2,1)
        grid.addWidget(self.view,0,3,4,5) #from row, from column, row-span, column-span
        
        grid.setContentsMargins(20,0,20,0)
        grid.setColumnMinimumWidth(2,200)
        
        
    def connect_signals(self):
        '''
        Adjusts and connects all the created widgets' signals to their respective slots(functions) and edits their properties
        '''
        #sliders:
        self.slider1.setMinimum(0)
        self.slider2.setMinimum(0)
        self.slider1.setMaximum(360)
        self.slider2.setMaximum(360)
        self.slider1.setTracking(True)
        self.slider2.setTracking(True)
        self.slider1.valueChanged.connect(self.view.arms[0].rotate)
        self.slider2.valueChanged.connect(self.view.arms[1].rotate)
        self.slider1.setTickPosition(QSlider.TicksBelow)
        self.slider2.setTickPosition(QSlider.TicksBelow)
        
        #line_edits:
        validator = QDoubleValidator(0,360,4) #accepts only float values between 0, 360 and up to 4 decimal places
        self.line_e1.setValidator(validator)
        self.line_e1.setPlaceholderText("Enter number between 0-360")
        self.line_e1.returnPressed.connect(lambda: self.check_line_edit(self.line_e1.text(), 0))
        self.line_e2.setValidator(validator)
        self.line_e2.setPlaceholderText("Enter number between 0-360")
        self.line_e2.returnPressed.connect(lambda: self.check_line_edit(self.line_e2.text(), 1))

        #box control buttons:
        self.add_box_btn.clicked.connect(self.view.add_box)
        self.grab_btn.toggled.connect(self.view.define_grab)
        
        #the text edit widget:
        self.text_edit.setMaximumHeight(600)
        self.text_edit.setMaximumWidth(300)
        self.text_edit.setProperty("plainText", "")
        self.text_edit.setPlaceholderText("Enter commands as 1:270 where\n"
                                          "1 = the arm number (1 or 2)\n"
                                          ": = separator\n"
                                          "270 = desired angle\n"
                                          "Enter one command per line\n"
                                          "Use the decimal point for float values\n"
                                          "Run the command with Ctrl+R\n")
                                            
        self.shortcut = QShortcut(QKeySequence("Ctrl+r"),self)#creates a shortcut to "run" the code in the textedit field
        self.shortcut.activated.connect(lambda: self.run_text(self.text_edit.toPlainText()))
        
        
    def run_text(self,text):
        '''
        This method is called when the user runs the code in the text edit field with Ctrl + r. It takes the string in the
        field, and chops it down to single commands for the arms, and checks for any errors in the commands. A message box alert
        is created, if an incorrect command is found. If the commands are correct, the methods hands them to the DrawWindow, which
        animates them.
        '''
        text_temp = text.split("\n")
        arm1_moves = []
        arm2_moves = []
        text = [e for e in text_temp if e != '']#remove blank lines
        
        try:
            for i in text:
                command = i.split(":")
                arm = int(command[0])
                value = float(command[1])
                if self.check_command(arm, value): #checks that the commands are correct
                    if arm == 1:
                        arm1_moves.append(value)
                    elif arm == 2:
                        arm2_moves.append(value)
                else:
                    arm1_moves.clear()
                    arm2_moves.clear()
                    
            number_of_moves = len(arm1_moves) + len(arm2_moves)
            self.view.animate_from_text(number_of_moves, arm1_moves, arm2_moves) #moves to the view for the animation
            if len(arm1_moves) != 0: #the sliders' positions are updated to the last command, for clarity
                self.slider1.setValue(arm1_moves[-1])
            if len(arm2_moves) !=0:
                self.slider2.setValue(arm2_moves[-1])
                
        except:
            self.alert_message("Incorrect command in text field. Please use only numbers, and enter the commands as instructed")
        
        
    def check_command(self,arm,value):
        '''
        The run_text method uses this method to check that individual commands are correct
        '''
        list_of_arms = [1,2]
        if arm not in list_of_arms:
            self.alert_message("Invalid arm number in text field")
            return False
        elif value > 360 or value < 0:
            self.alert_message("Invalid rotation angle in text field")
            return False
        else:
            return True


    def check_line_edit(self,text,arm):
        '''
        This method is used to verify the angle in the line edit class is valid, and pass the info to the animations and sliders.
        A message box alert is created if an incorrect value is found
        '''
        try:
            value = float(text)
            self.view.animate(value,arm)
            if arm == 0:
                self.slider1.setValue(value)
            elif arm == 1:
                self.slider2.setValue(value)
        except ValueError:
            self.alert_message("Enter only float numbers using the decimal point")
                

    def alert_message(self,text):
        '''
        Creates a QMessageBox alert window with the text
        '''
        self.message = QMessageBox()
        self.message.setWindowTitle("ERROR")
        self.message.setWindowIcon(QIcon(QPixmap("stop.png")))

        self.message.setText(text)
        self.message.exec()
                