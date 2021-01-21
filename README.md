# HMI code Information
**Last Update: May 1, 2020**

Run homeScreen.py to start the program

### File Functions
#### homeScreen.py
Runs the HMI program. The homescreen shows the cycle count and estimated finish time as well as start and stop buttons.
All the other screens can be accessed from this GUI.

#### Cycles.py
This file saves all the data for the HMI. 

#### LoadSet.py
The GUI that is called to set the static load. Only two buttons appear on this. Switch cylinder button that changes the airflow from one side to the other. And the STOP button that stops all airflow and closes the window.

#### otherSettingScreen.py
GUI that when called allows the human to change the folloing settings
- Staggered or Continuous runtime
    - Time on and time off
- Thump on a timer or Cycle after input

#### piOut.py
This controlls the inputs and outputs from the pi.

#### resetScreen.py
GUI that allows the user to reset the cycle count to 0 and the limit to a number of their choice

#### sendMail.py
When this method is called, an email is sent to email addresses in the file. Edit this file to add or remove emails from the list

#### timeScreen.py
GUI which allows the setting of retract and extend time.

#### fakeSendMail.py
A replacement for sendMail.py. Is active when not on a linux computer. This allows testing without sending an email when the count is done.

#### lapOut.py

