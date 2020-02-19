PROJECT: Robot Arm
CREATED BY: Eero Asikainen
-------------------------------------------------------------------------------------------------
ABOUT:
This program creates a 2D-robot arm simulation using the PyQt5 graphical library. The user can manipulate the robot and create and grab 
objects. Movement is animated and can be adjusted from the user interface.
-------------------------------------------------------------------------------------------------
FILES:
The program files are located in the src-folder including two picture files. Documentation of the project is located in the doc-folder.
-------------------------------------------------------------------------------------------------
DEPENDENCIES:
Language used: Python 3.7.0

Modules:
-PyQt5
-sys
-random

of which PyQt5 needs to be installed separately.
-------------------------------------------------------------------------------------------------
MANUAL:
The program is run by running the "main_window.py" file. This opens the GUI in which the robot is located on the right side and sliders
and textfields are on the left. The user can manipulate the robots arms by eihter:

-Adjusting the sliders mith the mouse
-Writing a specific angles in the small text fields (0-360) and pressing the enter key
-Writing commands in the lower large text field. Commands are of the format "armnumber:value" like "2:60" which will set the angle of 
arm 2 to 60. Mulitple commands can be written, each on their own row. The commands can be run by pressing CTRL + R.

Box objects can be added to the field with the "Add box" button. A box will spawn in a random location. The box can be moved with the mouse.
When pushing the "Grab" button, the robot will try to grab a a box with its arm, and will continue to move it until the "Grab" button is 
pressed again, releasing the grab. The boxes on the field can be removed from the options, or by pressing the DEL key.

In the options, the user can set the animation duration, which will set the time of a single animation in milliseconds. Only positive integer values
less than 20 000 are accepted.
