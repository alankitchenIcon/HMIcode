 # The window that gives access to the settings of:
 # Stagger/Continuous runtime
 # Thump without waiting for an input or cycle switching when an input is detected
 # number pad to set the time the thumper runs and then pauses
 # and a button to revert back to the default settings

import tkinter as tk
from Cycles import Data
import platform

class Other:

    def __init__(self, data=Data()):
        self.data = data
        self.window = "0" # Becomes the main window
        self.cycle_thump_label = "0" # Becomes a label
        self.number_display = "0" # Becomes Label object for numberpad
        self.number_entry = "0" # The number string being added to by the number pad
    
    def show(self):

        # Set up the window
        self.window = tk.Tk()
        self.window.title("Other Settings")
        self.window.geometry("800x500")

        #Full Screen Settings
        if platform.system() == "Linux":
            self.is_fullscreen = True
        else:
            self.is_fullscreen = False
        self.window.attributes("-fullscreen", self.is_fullscreen)

        # Number pad for setting time on and off
        self.number_display = tk.Label(self.window, fg="red", text=self.number_entry)
        self.number_display.grid(row=0, column=0, columnspan=3)
        
        keys = [
            ['1', '2', '3'],    
            ['4', '5', '6'],    
            ['7', '8', '9'],    
           ['DEL', '0', ' . '],    
        ]

        # Make set of 12 buttons to act as number pad

        for x in range(0, 4):
            for y in range(0,3):
                button = tk.Button(self.window, text=keys[x][y],  command=lambda num=keys[x][y] : self.__number(num))
                button.grid(row = x + 1, column = y, ipadx=15, ipady=15)
                if keys[x][y] == "DEL":
                    button.grid(ipadx=8)
        

        # Display the current setttings on the left
        self.cycle_thump_label = tk.Label(self.window, text=self.data.mode)
        self.cycle_thump_label.grid(row=0, column=4, padx=10, pady=5)
        
        self.runtime_label = tk.Label(self.window, text=self.data.runtime)
        self.runtime_label.grid(row=1, column=4, padx=10, pady=5)

        # Display of the Stagger times below the other buttons
        on_time_text = tk.Label(self.window, text="Time On (min)")
        on_time_text.grid(row=2, column=4, padx=10, pady=5)

        off_time_text = tk.Label(self.window, text="Time Off (min)")
        off_time_text.grid(row=3, column=4, padx=10, pady=5)

        self.on_time_number = tk.Label(self.window, text=self.data.stagger_on / 60000)
        self.on_time_number.grid(row=2, column=5, padx=10, pady=5)

        self.off_time_number = tk.Label(self.window, text=self.data.stagger_off / 60000)
        self.off_time_number.grid(row=3, column=5, padx=10, pady=5)

        # Toggle buttons to the right of the Labels
        cycle_thump_button = tk.Button(self.window, text="Cycle/Thump Toggle", command=self.__toggle_thump_cycle)
        cycle_thump_button.grid(row=0, column=5, padx=10, pady=5)

        runtime_button = tk.Button(self.window, text="Continuous/Stagger Runtime", command=self.__toggle_continuous_Stagger)
        runtime_button.grid(row=1, column=5, padx=10, pady=5)

        revert_settings_button = tk.Button(self.window, text="Revert to Default Settings", command=self.__revert_settings)
        revert_settings_button.grid(row=4 ,column=5, ipadx=10, ipady=5)

        # Set time Buttons
        on_time_button = tk.Button(self.window, text="Set Time On", command=self.__set_time_on)
        on_time_button.grid(row=2, column=6, padx=10, pady=5)

        off_time_button = tk.Button(self.window, text="Set Time Off", command=self.__set_time_off)
        off_time_button.grid(row=3, column=6, padx=10, pady=5)

        #Done button
        done_button = tk.Button(self.window, text="DONE", command=self.__quit_window, bg="blue")
        done_button.grid(row=5, column=6,columnspan=2, ipadx=20, ipady=15)

        self.window.protocol("WM_DELETE_WINDOW", self.__quit_window)
        self.window.mainloop()

    def __number(self, x):
        # Command for each number on the pad

        if x == "DEL":
            if self.number_entry == "0":
                self.number_entry = "0"
            elif self.number_entry == self.number_entry[0]:
                self.number_entry = "0"
            else:
                self.number_entry = self.number_entry[:-1]
    
        elif x == " . ":
            if "." in self.number_entry:
                self.number_entry = self.number_entry
            else:
                self.number_entry = self.number_entry + "."

        else: # Number Entry
            if self.number_entry == "0":
                self.number_entry = x
            else:
                self.number_entry = self.number_entry + x
        self.number_display.config(text=self.number_entry)
    

    def __toggle_continuous_Stagger(self):
        # Changes the setting where the thump is continuous or stops after so long.
        if self.data.runtime == "Stagger":
            self.data.runtime = "Continuous"
        elif self.data.runtime == "Continuous":
            self.data.runtime = "Stagger"
        self.runtime_label.config(text=self.data.runtime)

    def __toggle_thump_cycle(self):
        # Changes the setting if the pi thumps without waiting for inputs or cycles and changes when the magnets are activated.
        if self.data.mode == "Thump":
            self.data.mode = "Cycle"
        elif self.data.mode == "Cycle":
            self.data.mode = "Thump"
        self.cycle_thump_label.config(text=self.data.mode)

    def __quit_window(self):
        # closes the window
        self.window.destroy()
        self.window.quit()

    def __set_time_on(self):
        # Applies the number displayed to the time on setting
        self.data.stagger_on = int(float(self.number_entry) * 60000)
        self.on_time_number.config(text=self.data.stagger_on / 60000)
        # The 60000 is to convert minutes into miliseconds

    def __set_time_off(self):
        # Applies the number displayed to the time off setting
        self.data.stagger_off = int(float(self.number_entry) * 60000)
        self.off_time_number.config(text=self.data.stagger_off / 60000)
    
    def __revert_settings(self):
        # Sets all the settings back to the set default settings
        self.data.revert_default()
        self.off_time_number.config(text=self.data.stagger_off / 60000)
        self.on_time_number.config(text=self.data.stagger_on / 60000)
        self.cycle_thump_label.config(text=self.data.mode)
        self.runtime_label.config(text=self.data.runtime)