# This ONLY works on a raspberry pi
# This file has the outputs that flip the relays and read the inputs
from RPi import GPIO as pi


class piControl:

    def __init__(self, x, y, xi, yi):
        self.right = x
        self.left = y
        self.righti = xi
        self.lefti = yi

        # Setup of the Pi to produce outputs
        pi.setwarnings(False)
        pi.setmode(pi.BCM) # Numbering system of the pins
        pi.setup([self.left, self.right], pi.OUT) # Output pins
        pi.setup([self.lefti, self.righti], pi.IN) # Inputs pins

    def leftOn(self):
        pi.output(self.left, True)

    def rightOn(self):
        pi.output(self.right, True)

    def off(self):
        # Turns both outputs off
        pi.output([self.right, self.left], False)
        
    def leftIn(self):
        return (pi.input(self.lefti) == 1)
    
    def rightIn(self):
        return (pi.input(self.righti) == 1)

