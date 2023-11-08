from tkinter import *

class View:
    def __init__(self, controller):
        self.controller = controller

        # creating window
        self.window_setup()

    def window_setup(self):
        
        # creating main window
        self.window = Tk()

    def update(self):
        self.window.update()