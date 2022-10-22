from tkinter import ttk
import tkinter as tk
from functools import partial

class ParamsPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        paramsLabel = ttk.Label(
            self,
            text="View and Modify Parameters"
            ).grid(row=0,column=0,columnspan=2,pady=5)

        mode = StringVar(self)
        mode.set("AOO")
        
        pacingModes = ttk.OptionMenu(
            self,
            mode,
            "AOO", "VOO", "AAI", "VVI"
            )
        pacingModes.pack()
        pacingModes.grid(row=1,column=0,columnspan=2)

        #Parameters to display:
            #Lower Rate Limit: all
            #Upper Rate Limit: all
            #Atrial Amplitude: AOO, AAI
            #Atrial Pulse Width: AOO, AAI
            #Ventricular Amplitude: VOO, VVI
            #Ventricular Pulse Width: VOO, VVI
            #VRP: VVI
            #ARP: AAI