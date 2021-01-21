# This screen is to reset the cycle count and max cycle limit
import tkinter as tk
from Cycles import Data
import platform

class resetScreen:

    def __init__(self, cycle=Data()):
        self.cycle_data = cycle
        self.number_entry = "0"
        self.number_display = 0
        self.window = None
        self.cycle_limit_number = None

    def show(self, cycle):
        # Method used to actually show the window
        self.cycle_data = cycle
        self.window = tk.Tk()
        self.window.title("Set Cycle Count")
        self.window.geometry("700x500")
        self.number_display = tk.Label(self.window, text=self.number_entry)
        self.number_display.grid(row=0, column=0, columnspan=3)

        if platform.system() == "Linux":
            self.is_fullscreen = True
        else:
            self.is_fullscreen = False
        self.window.attributes("-fullscreen", self.is_fullscreen)

        if platform.system() == "Linux":
            self.window.config(cursor="none")
        

        keys = [
            ['1', '2', '3'],    
            ['4', '5', '6'],    
            ['7', '8', '9'],    
           ['DEL', '0', 'CLR'],    
        ]

        
# Make set of 12 buttons to act as number pad

        for x in range(0, 4):
            for y in range(0,3):
                button = tk.Button(self.window, text=keys[x][y],  command=lambda num=keys[x][y] : self.__number(num))
                button.grid(row = x + 1, column = y, ipadx=15, ipady=15)
                if keys[x][y] == "DEL" or keys[x][y] == "CLR":
                    button.grid(ipadx=8)

# Labels that display current Cycle Values
        cycle_limit_text = tk.Label(self.window, text="Cycle Limit")
        cycle_limit_text.grid(row=1, column=3)

        self.cycle_limit_number = tk.Label(self.window, text=self.cycle_data.max)
        self.cycle_limit_number.grid(row=2, column=3)

        cycle_count_text = tk.Label(self.window, text="Cycle Count")
        cycle_count_text.grid(row=1, column=4)

        self.cycle_count_number = tk.Label(self.window, text=self.cycle_data.count)
        self.cycle_count_number.grid(row=2, column=4)

# Buttons to reset the Cycle Count and Cycle Limit
        reset_limit = tk.Button(self.window, text="Set Limit", command=self.__limit)
        reset_limit.grid(row=3, column=3)

        done_button = tk.Button(self.window, text="Done", command=self.__done_action, bg="Blue")
        done_button.grid(row=5, column=5, columnspan=2, ipadx=20, ipady=15)

        reset_count = tk.Button(self.window, text="Set Count 0", command=self.__count_to_zero)
        reset_count.grid(row=3, column=4)

        # Common Cycle count values
        k500 = tk.Button(self.window, text="500 k", command= lambda : self.__common(500000))
        k500.grid(row=5, column=0, ipady=15, ipadx = 7)

        m1 = tk.Button(self.window, text="1 mil", command = lambda : self.__common(1000000))
        m1.grid(row=5, column=1, ipady=15, ipadx=8)

        m12 = tk.Button(self.window, text="1.2 mil", command=lambda : self.__common(1200000))
        m12.grid(row=5, column=2, ipady=15, ipadx=6)

        m3 = tk.Button(self.window, text="3 mil", command=lambda : self.__common(3000000))
        m3.grid(row=5, column=3, ipady=15, ipadx=8)

        self.window.protocol("WM_DELETE_WINDOW", self.__done_action)
        self.window.mainloop()


# Commands
    def __number(self, x):
    # Commands for when each number is pressed
        if x == "DEL":
            if self.number_entry == "0":
                self.number_entry = "0"
            elif self.number_entry == self.number_entry[0]:
                self.number_entry = "0"
            else:
                self.number_entry = self.number_entry[:-1]
    
        elif x == "CLR":
            self.number_entry = "0"

        else: # Number Entry
                if self.number_entry == "0":
                    self.number_entry = x
                else:
                    self.number_entry = self.number_entry + x
        self.number_display.config(text=self.number_entry)
    
    def __common(self, number):
        self.number_entry = str(number)
        self.number_display.config(text=self.number_entry)
        self.__limit()

    def __limit(self):
        # Sets the Cycle limit to the number shown
        if self.number_entry.isdigit():
            self.cycle_data.max = int(self.number_entry)
        self.cycle_limit_number.config(text=self.cycle_data.max)

    def __done_action(self):
        # Closes the window
        self.window.destroy()
        self.window.quit()

    def __count_to_zero(self):
        # Resets the cycle count to 0
        self.cycle_data.count = 0
        self.cycle_count_number.config(text=self.cycle_data.count)
        