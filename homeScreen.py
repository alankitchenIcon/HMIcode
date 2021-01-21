# This runs the home screen 

import tkinter as tk
from resetScreen import resetScreen
from Cycles import Data
from timeScreen import timeSet
from otherSettingScreen import Other
import platform
if platform.system() == "Linux":
    import piOut as outputs
    import sendMail as mail
else:
    import lapOut as outputs
    import fakeSendMail as mail
import LoadSet
from datetime import datetime, timedelta
from time import time, sleep
import math

class home:
    def __init__ (self):
        # Control the outputs and inputs initialized
        self.out = outputs.piControl(14, 15, 23, 24)

        # The data and settings information is initialized
        self.cycle_data = Data()
        self.finish_date = 0

        # The subscreens are initialized so "show" can be called on them later
        self.reset_data = resetScreen(self.cycle_data)
        self.time_data = timeSet(self.cycle_data)
        self.load = LoadSet.SettingLoad(self.out)
        self.other_settings = Other(self.cycle_data)

        # Data that helps control the cycles run and switch
        self.cycle_side = True
        self.previous_cycle_side = False
        self.finish_update = True

        # Initializing the Main Window
        self.window = tk.Tk()
        self.window.title("Data Home Screen")

        
        # Jobs that need to be able to be cancelled in other methods
        self.job = self.window.after(0, self.__nothing)
        self.stagger = False
        self.stagger_job = self.window.after(0, self.__nothing)
        self.sensing = False

        # Miscellanies things to help the screen look better
        self.fontsize = 18
        self.is_fullscreen = True
        if platform.system() == "Linux":
            self.window.config(cursor="none") #Hides the mouse when on the Pi
            self.is_fullscreen = True
        else:
            self.is_fullscreen = False
        
        # Labels on main screen window
        cycle_count_text = tk.Label(self.window, text="Cycle Count", font=(None, self.fontsize))
        cycle_count_text.grid(row=1, column=0)

        cycle_limit_text = tk.Label(self.window, text="Cycle Limit", font=(None, self.fontsize))
        cycle_limit_text.grid(row=2, column=0, pady=3)

        time_remaining_text = tk.Label(self.window, text="Estimated Finish", font=(None, self.fontsize))
        time_remaining_text.grid(row=4, column=0)

        cycle_rate_text = tk.Label(self.window, text="Cycle Rate", font = (None, self.fontsize))
        cycle_rate_text.grid(row=3, column=0)

        # Labels that need to be accessed by methods to change the counts
        self.cycle_limit_number = tk.Label(self.window, text=self.cycle_data.max, font=(None, self.fontsize))
        self.cycle_limit_number.grid(row=2, column=1)

        self.cycle_count_number = tk.Label(self.window, text=self.cycle_data.count, font=(None, self.fontsize))
        self.cycle_count_number.grid(row=1, column=1, pady=3)

        self.time_remaining_number = tk.Label(self.window, text="N/A", font=(None, self.fontsize))
        self.time_remaining_number.grid(row=4, column=1)

        self.cycle_rate_number = tk.Label(self.window, text=self.cycle_data.cycle_rate, font=(None, self.fontsize))
        self.cycle_rate_number.grid(row=3, column = 1)

        # Buttons on the Home Screen
        self.start_Button = tk.Button(self.window, text="START", bg="Green", command=self.__start, font=(None, self.fontsize), activebackground="Green")
        self.start_Button.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.start_Button.config(height=7, width=21)

        stop_Button = tk.Button(self.window, text="STOP", bg="Red", command=self.__stop, font=(None, self.fontsize), activebackground="Red")
        stop_Button.grid(row=0, column=2, padx=10, pady=10, columnspan=2)
        stop_Button.config(height=7, width=21)

        # If an emergency stop is needed, this can be uncommented, I believe there is no need for this.
        # emergency_stop_Button = tk.Button(self.window, text="Emergency Stop", bg="black", fg="red", font=(None, self.fontsize),command=self.__emergency_stop, activebackground="black", activeforeground="Red")
        # emergency_stop_Button.grid(row=4, column=0, rowspan=2, ipady=10)

        reset_Button = tk.Button(self.window, text="Cycle Settings", command=self.__reset_settings, font=(None, self.fontsize))
        reset_Button.grid(row=5, column=1, columnspan=1, ipadx=10, ipady=5)

        time_Button = tk.Button(self.window, text="Time Settings", command=self.__time_action, font=(None, self.fontsize))
        time_Button.grid(row=5, column=2, columnspan=1, ipadx=10, ipady=5)

        other_settings_button = tk.Button(self.window, text="Other Settings", command=self.__other_settings, font=(None, self.fontsize))
        other_settings_button.grid(row=5, column=0, ipadx=10, ipady=5)

        set_load_button = tk.Button(self.window, text="To Set Load", command=self.__load, font=(None, self.fontsize))
        set_load_button.grid(row=2, column=2)

        end_fullscreen_button = tk.Button(self.window, text="ESC", command=self.__close_fullscreen, font=(None, self.fontsize))
        end_fullscreen_button.grid(row=5, column=3)

        # Full Screen Settings
        self.window.bind("<Escape>", self.__close_fullscreen)
        self.window.bind("<F11>", self.__toggle_fullscreen)
        self.window.attributes("-fullscreen", self.is_fullscreen)
        
        if self.cycle_data.mode == "Cycle":
            self.start_Button.config(command=self.__cycleStart)
            self.sensing = True
            self.__cycle_inputs()
        # Run the window loop
        self.window.mainloop()

# Commands that go with Buttons
    def __start(self):

        self.__get_cycle_rate()       

        # Start button for the thump test mode
        if self.cycle_data.count % 1000 == 0:
            self.cycle_data.save()
            self.__change_finish_date()
        if self.cycle_data.count >= self.cycle_data.max:
            self.__stop()
            # mail.send() # This could be uncommented to send an email when the cycle limit is reached
            return
        if self.finish_update:
            self.__change_finish_date()
        if self.stagger:
           self.stagger_job = self.window.after(self.cycle_data.stagger_on, self.__pause)
           self.stagger = False
        self.out.off()
        self.out.rightOn()
        self.window.after(self.cycle_data.extend_time)
        self.out.off()
        self.out.leftOn()
        self.cycle_data.increment()
        self.__update_count()
        self.__update_cycle_rate()
        self.job = self.window.after(self.cycle_data.retract_time, self.__start)
        

    def __cycleStart(self):


        # Start Command when the cycle mode is selected
        if self.cycle_data.count % 100 == 0:
            self.__change_finish_date_cycle()
        if self.cycle_data.count >= self.cycle_data.max:
            self.__stop()
            return
        if self.cycle_side:
            if not self.previous_cycle_side:
                self.previous_cycle_side = self.cycle_side
                self.cycle_data.increment()
                self.__update_count()
                self.__get_cycle_rate()
                self.__update_cycle_rate()
                self.out.off()
                self.out.rightOn()
        elif not self.cycle_side:
            if self.previous_cycle_side:
                self.out.off()
                self.out.leftOn()
                self.previous_cycle_side = self.cycle_side
        self.job = self.window.after(1, self.__cycleStart)


    def __update_count(self):
        # Changes the display to the correct current cycle number
        self.cycle_count_number.config(text=self.cycle_data.count)
    
    def __update_cycle_rate(self):
        #Changes the display to the correct & current cycle rate
        self.cycle_rate_number.config(text=self.cycle_data.cycle_rate)

    def __stop(self):
        # Stops all actions
        self.out.off()
        self.window.after_cancel(self.job)
        self.cycle_side = True
        self.previous_cycle_side = False
        self.window.after_cancel(self.stagger_job)
        self.stagger = (self.cycle_data.runtime == "Stagger")
        self.finish_date = 0
        self.time_remaining_number.config(text="N/A")
        self.cycle_data.save()


    def __emergency_stop(self):
        # Stops all processes, closes the window, and then opens a new window
        self.out.off()
        self.window.after_cancel(self.job)
        self.cycle_data.save()
        self.window.destroy()
        self.window.quit()
        home()


    def __pause(self):
        self.out.off()
        self.window.after_cancel(self.job)
        print("Pause")
        self.stagger = True
        self.window.after(self.cycle_data.stagger_off, self.__start)
        self.cycle_data.save()


    def __reset_settings(self):
        # Opens the window to change the cycle count
        # The display is changed once the other window is closed
        self.__stop()
        self.reset_data.show(self.cycle_data)
        self.cycle_limit_number.config(text=self.cycle_data.max)
        self.cycle_count_number.config(text=self.cycle_data.count)
        self.cycle_data.save()


    def __time_action(self):
        # Opens the window to change the time settings
        self.__stop()
        self.time_data.show()
        self.cycle_data.save()
        # No time information shown on main Screen


    def __close_fullscreen(self, Event=None):
        # Closes the Fullscreen when <ESC> is pressed
        self.is_fullscreen = False
        self.window.attributes("-fullscreen", self.is_fullscreen)


    def __toggle_fullscreen(self, Event):
        # Toggles fullscreen when <F11> is pressed
        if self.is_fullscreen:
            self.is_fullscreen = False
        else:
            self.is_fullscreen = True
        self.window.attributes("-fullscreen", self.is_fullscreen)


    def __load(self):
        # Shows the set Load screen
        self.__stop()
        self.load.show()


    def __cycle_inputs(self):
        # Is to be run behind the Cycle Start method that detects the inputs
        if self.out.rightIn():
            self.cycle_side = True
        if self.out.leftIn():
            self.cycle_side = False
        if self.sensing:
            self.window.after(1, self.__cycle_inputs)


    def __other_settings(self):
        # Opens the Other settings window
        self.__stop()
        self.other_settings.show()
        if self.cycle_data.mode == "Thump":
            self.start_Button.config(command=self.__start)
            self.sensing = False
        elif self.cycle_data.mode == "Cycle":
            self.start_Button.config(command=self.__cycleStart)
            self.sensing = True
            self.__cycle_inputs()
        if self.cycle_data.runtime == "Stagger":
            self.stagger = True
        elif self.cycle_data.runtime == "Continuous":
            self.stagger = False
        self.cycle_limit_number.config(text=self.cycle_data.max)
        self.cycle_count_number.config(text=self.cycle_data.count)
        self.cycle_data.save()

    def __get_cycle_rate(self):

        deltaTime = time() - float(self.cycle_data.timeOf_last_count)
        self.cycle_data.cycle_rate = round(60/deltaTime, 2)
        self.cycle_data.timeOf_last_count = time()

    def __calculate_time(self):
        # Returns the number of days left according to the extend and retract time.
        remaining = (self.cycle_data.retract_time + self.cycle_data.extend_time) * (self.cycle_data.max - self.cycle_data.count)
        remaining = remaining / 1000
        now = datetime.today()
        finish = now + timedelta(seconds=remaining)
        self.finish_date = finish.strftime("%m/%d/%Y %H:%M")


    def __change_finish_date(self):
        self.__calculate_time()
        self.time_remaining_number.config(text=self.finish_date)

    def __change_finish_date_cycle(self):
        now = datetime.today()
        remaining = ((self.cycle_data.max - self.cycle_data.count)/self.cycle_data.cycle_rate)*60
        finish = now + timedelta(seconds = remaining)
        self.finish_date = finish.strftime("%m/%d/%Y %H:%M")
        self.time_remaining_number.config(text = self.finish_date)

    def __nothing(self):
        pass

test = home()
