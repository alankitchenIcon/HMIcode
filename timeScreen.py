# This screen is to set the extend and retract time of the thump test

import tkinter as tk
from Cycles import Data
import platform

class timeSet:

    def __init__(self, data = Data()):
        self.data = data
        self.number_entry = "0" # This is the number that is shown above the number pad
        self.number_display = "0" # This becomes the Button object in show(self)
        self.extend_time_number = "0" # This becomes the Label object
        self.retract_time_number = "0" # This becomes the Label object
        self.window = "0" #Becomes the main Window object

    def __retract(self):
        # The time one side of the cylinder is activated
        self.data.retract_time = int(float(self.number_entry) * 1000)
        self.retract_time_number.config(text=self.data.retract_time / 1000)

    def __extend(self):
        # The time the other side of the cylinder is activated
        self.data.extend_time = int(float(self.number_entry) * 1000) # The 1000 is to convert from seconds to miliseconds
        self.extend_time_number.config(text=self.data.extend_time / 1000)

    def __done(self):
        # Done button that closes the window
        self.window.destroy()
        self.window.quit()

    def __number(self, x):
        # The command of each button when it is pressed
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

    def show(self):
        # The command that the home screen calls to show this time screen

        self.window = tk.Tk()
        self.window.title("Time Settings")
        self.window.geometry("700x500")

        #Fullscreen Setup
        if platform.system() == "Linux":
            self.is_fullscreen = True
        else:
            self.is_fullscreen = False
        self.window.attributes("-fullscreen", self.is_fullscreen)

        if platform.system() == "Linux":
            self.window.config(cursor="none")
        self.number_display = tk.Label(self.window, text=self.number_entry)
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
        
        # Text on the screen
        retract_time_text = tk.Label(self.window, text = "Retract Time (s)")
        retract_time_text.grid(row=1, column=3)
        
        self.retract_time_number = tk.Label(self.window, text = self.data.retract_time / 1000)
        self.retract_time_number.grid(row=2, column=3)

        extend_time_text = tk.Label(self.window, text = "Extend Time (s)")
        extend_time_text.grid(row=1, column=4)

        self.extend_time_number = tk.Label(self.window, text=self.data.extend_time / 1000)
        self.extend_time_number.grid(row=2, column=4)

        #Buttons on the window
        retract_button = tk.Button(self.window, text="Set Retract", command=self.__retract)
        retract_button.grid(row=3, column=3)

        extend_button = tk.Button(self.window, text="Set Extend", command=self.__extend)
        extend_button.grid(row=3, column=4)

        done_button = tk.Button(self.window, text="Done", command=self.__done, bg="blue")
        done_button.grid(row=5, column=3, columnspan=2, ipady=15, ipadx=20)

        self.window.protocol("WM_DELETE_WINDOW", self.__done)
        self.window.mainloop()

