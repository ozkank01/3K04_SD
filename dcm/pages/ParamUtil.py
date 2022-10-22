#utility to view and modify each parameter
from tkinter import ttk
import tkinter as tk
from functools import partial

class ParamUtil(tk.Frame):
    


    def __init__(self,parent,controller,label,r):
        super().__init__(parent)

        self.r = r

        self.paramLabel = ttk.Label(
            self,
            text=label
        ).grid(row=self.r,column=0)

        self.pButton = ttk.Button(
            self,
            text="Modify",
            command=self.modify()
        ).grid(row=self.r,column=1)
        
        self.newVal = ttk.Entry(
            self,
            textvariable=self.r
        ).grid_remove()

        self.valButton = ttk.Button(
            self,
            text="OK",
            command=self.doneModify()
        ).grid_remove()

    def modify(self):
        newValue = tk.StringVar()
        self.newVal.grid(row=self.r,column=2)
        self.valButton.grid(row=self.r,column=3)

    def doneModify(self):
        self.newVal.grid_remove()
        self.valButton.grid_remove()