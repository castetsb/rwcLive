# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
from tkinter import *
from tkinter import ttk
import numpy as np
import requests
from matplotlib import pyplot as plt
from PIL import ImageTk, Image


class RwcLive(Tk):
    """
    Graphic interface to visualize Robotiq Wrist Camera live image.
    """
    
    def __init__(self, master=None):
        """
        Graphic interface to visualize Robotiq Wrist Camera live image.
        """
        super().__init__()
        
        #GUI ayout manager
        self.grid()
        
        #Configuration
        ##############
        self.title("Robotiq Wrist Camera Live Viewer")
        
        
        #Variables
        ##########
        #Ip of the robot
        self.ipValue = StringVar()
        #Last image retrieved from the camera in Tkinter format
        self.tkImage=None
        
        
        #GUI elements
        #############
        self.mainframe=None
        self.imgLabel=None
        
        #Build the GUI Widgets
        ######################
        self.createWidgets()
        
        #Start the video streaming
        ######################
        self.streamVideo()
    
    def streamVideo(self):
        """
        Retrieve Robotiq wrist camera image and display it in the GUI
        """
        
        #Varaibles
        ##########
        #HTTP request response
        resp=None
        #Retrieved image in Tkinter format
        tkImage=None
        
        #Try to get camera image with provided robot IP
        try:
            resp = requests.get("http://"+self.ipValue.get()+":4242/current.jpg?type=color").content
        except:
            pass
            
            
        if resp is not None:
            image = np.asarray(bytearray(resp), dtype="uint8")
            npImage = cv2.imdecode(image, cv2.IMREAD_COLOR)
            pilImage=Image.fromarray(npImage)
            tkImage = ImageTk.PhotoImage(pilImage)
        else:
            pilImage=Image.open("error.jpg")
            tkImage = ImageTk.PhotoImage(pilImage)
            
        self.imgLabel.tkImage=tkImage
        self.imgLabel.configure(image=tkImage)
        self.imgLabel.after(100, self.streamVideo)

    def createWidgets(self):
        """
        Create application widgets
        """
        
        #Main Frame
        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        #Instruction to complete Robot IP field
        self.imgLabel=ttk.Label(self.mainframe, text="Enter robot IP address")
        self.imgLabel.grid(column=1, row=1, sticky=(W, E))
        
        #Entry field for Robot IP
        self.ip_entry = ttk.Entry(self.mainframe, textvariable=self.ipValue)
        self.ip_entry.grid(column=1, row=2, sticky=(W, E))
        
        #Image container to display the camera image
        self.imgLabel=ttk.Label(self.mainframe)
        self.imgLabel.grid(column=1, row=3, sticky=(W, E))
        
if __name__ == "__main__": 
    app = RwcLive()  
    app.mainloop()