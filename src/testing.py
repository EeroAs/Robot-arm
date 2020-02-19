import unittest
from main_window import MainWindow
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

app = QtWidgets.QApplication(sys.argv)

class Test(unittest.TestCase):
    '''
    This is a unittest for some functionality of the robot arm program. It uses python's own unittest library
    as well as the QTest methods from PyQt5. A QApplication is created above the class, in order to have a single
    app which all the tests can use.
    '''

    def setUp(self):
        '''
        Setup-function for the tests, where gui is an instance of Gui() from gui.py and 
        view is a DrawWindow() from draw_window.py
        '''
        self.window = MainWindow()
        self.gui = self.window.centralWidget()
        self.view = self.window.centralWidget().view
        self.reset_all()
        
        
    def tearDown(self):
        self.window.close()
        
        
    def test_arm_rotation(self):
        "This test checks if the basic rotate function of ArmObject is working"
        self.view.arms[0].rotate(90)
        self.view.arms[1].rotate(100)
        self.assertEqual(90, self.view.arms[0].arm.rotation(), "Rotation of arm 1 was not 90 degrees")
        self.assertEqual(100, self.view.arms[1].arm.rotation(), "Rotation of arm 2 was not 100 degrees")
        
        
    def test_sliders(self):
        "This test checks if the sliders change the values of the arms correctly"
        self.gui.slider1.setValue(180)
        self.gui.slider2.setValue(50)
        self.assertEqual(180, self.view.arms[0].arm.rotation(), "Slider1 set incorrect value")
        self.assertEqual(50, self.view.arms[1].arm.rotation(), "Slider2 set incorrect value")
        
    
    def test_sliders_maximum(self):
        "This test checks that the sliders maximum values are correct"
        self.gui.slider1.setValue(361)
        self.gui.slider2.setValue(-1)
        self.assertEqual(self.gui.slider1.value(),360, "Slider1 max-value incorrect")
        self.assertEqual(self.gui.slider2.value(),0, "Slider2 min-value incorrect")
        

    def test_adding_boxes(self):
        "This test checks if the add box button adds a correct amount of boxes"
        QTest.mouseClick(self.gui.add_box_btn, Qt.LeftButton)
        QTest.mouseClick(self.gui.add_box_btn, Qt.LeftButton)
        self.assertEqual(len(self.view.boxes), 2, "Incorrect amount of boxes added with the add box btn")
        
        
    def test_deleting_boxes(self):
        "This test checks that the delete boxes function is working"
        QTest.mouseClick(self.gui.add_box_btn, Qt.LeftButton)
        QTest.mouseClick(self.gui.add_box_btn, Qt.LeftButton)
        self.view.delete_all_boxes()
        self.assertEqual(len(self.view.boxes), 0, "Deleting boxes was not successful")
        
        
    def test_text_edit(self):
        "This test checks if the text edit field handles commands correctly"
        self.gui.run_text("1:100\n1:200\n1:33\n2:40")
        self.assertEqual(33, self.view.arms[0].arm.rotation(), "Incorrect value from text edit field for arm 1")
        self.assertEqual(40, self.view.arms[1].arm.rotation(), "Incorrect value from text edit field for arm 2")
        
        
    def test_arm_relations(self):
        "This test checks that the child-parent relationships of items is correct"
        self.assertEqual(self.view.arms[1].arm.parentItem(), self.view.arms[0].arm, "Arm 2 is not a child of arm 1")
        
        
    def reset_all(self):
        "this function resets the values of all components, and should be ran in the setup before each test"
        self.gui.slider1.setValue(0)
        self.gui.slider2.setValue(0)
        self.gui.line_e1.setText("")
        self.gui.line_e2.setText("")
        self.gui.text_edit.setPlainText("")
        self.view.arms[0].arm.setRotation(0)
        self.view.arms[1].arm.setRotation(0)
        

if __name__ == "__main__":
    unittest.main()