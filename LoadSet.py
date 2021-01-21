# Makes the Screen that lets us set the load

import tkinter as tk
import platform
if platform.system() == "Darwin" or platform.system() == "Windows":
    import lapOut as outputs
else:
    import piOut as outputs

class SettingLoad:

    def __init__(self, output):
        self.out = output
        self.right = True
        self.window = "0" #Becomes window object first time show() is done 
        
    def show(self):
        
        # Window
        self.window = tk.Tk()
        self.window.title("Setting the Load")
        self.window.geometry("700x500")
        self.right = True

        # Fullscreen Settings
        if platform.system() == "Linux":
            self.is_fullscreen = True
        else:
            self.is_fullscreen = False
        self.window.attributes("-fullscreen", self.is_fullscreen)

        # Buttons
        switch_button = tk.Button(self.window, text="Switch Cylinder", command=self.__switch)
        switch_button.grid(row=0, column=0, ipadx=20, ipady=20, padx=30, pady=50)

        self.stop_button = tk.Button(self.window, text="OFF", bg = "red", command=self.__stop, activebackground="red")
        self.stop_button.grid(row=0, column=1, ipadx=20, ipady=20, padx=30, pady=50)

        done_button = tk.Button(self.window, text="DONE", bg="blue", command=self.__done, activebackground="blue")
        done_button.grid(row=1, column=0, columnspan=2, ipady=20, ipadx=30)

        self.__switch()
        self.window.protocol("WM_DELETE_WINDOW", self.__done)
        self.window.mainloop()

    def __switch(self):
        # Switches the activated load from one side to the other.
        self.out.off()
        if self.right:
            self.right = False
            self.out.leftOn()
        else:
            self.right = True
            self.out.rightOn()
    
    def __stop(self):
        # The stop button that shuts off the load and closes the window.
        self.out.off()
        self.stop_button.config(command=self.__start, bg="green", activebackground="green", text="ON")

    def __start(self):
        self.right = self.right == False
        self.__switch()
        self.stop_button.config(command=self.__stop, bg="red", activebackground="red", text="OFF")
    
    def __done(self):
        self.window.destroy()
        self.window.quit()