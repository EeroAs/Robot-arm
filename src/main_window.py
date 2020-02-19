from gui import Gui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMenuBar,QAction
import sys
from PyQt5.Qt import QIcon, QInputDialog
from PyQt5.QtGui import QPixmap

class MainWindow(QtWidgets.QMainWindow):
    '''
    This class is the main window of the program, it handles adding the Gui() as a widget, and creating a menu. Running the
    main_window.py module activates the program
    '''
    
    def __init__(self):
        super().__init__()
        self.setCentralWidget(Gui())
        self.setWindowTitle("Robot Arm")
        self.setWindowIcon(QIcon(QPixmap("ArmIcon.png")))
        self.resize(1500,800)
        self.add_menu()
        
        
    def add_menu(self):
        '''
        Adds the menubar to the window, add some functionality to it.
        '''
        menu = QMenuBar()
        self.setMenuBar(menu)
        options = menu.addMenu("Options")
        #actions:
        delete_boxes_action = QAction("Delete all boxes",self)
        delete_boxes_action.setShortcut('Del')
        set_animation_duration = QAction("Set the animation duration",self)
        #add actions to the menu
        options.addAction(delete_boxes_action)
        options.addAction(set_animation_duration)
        #connect actions to methods
        delete_boxes_action.triggered.connect(self.centralWidget().view.delete_all_boxes)
        set_animation_duration.triggered.connect(self.animation_duration)
        
    
    def animation_duration(self):
        '''
        This method is called when the user clicks set animation duration from the window opions menu. It creates an input for
        the animation duration, and accepts only positive integers as values
        '''
        value, ok = QInputDialog.getText(self,"Animation duration","Enter the duration in ms")
        if ok:
            try:
                value = int(value)
                if value <= 0:
                    raise Exception
                elif value > 20000:
                    raise Exception
                else:
                    self.centralWidget().view.set_animation_duration(value)
            except:
                self.centralWidget().alert_message("Incorrect duration entered. Give duration as an positive integer and below 20000")
        
        
'''
code after this is for showing the window
------------------------------------------------------------
'''
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    new_window = MainWindow()
    new_window.show()
    sys.exit(app.exec_())
        