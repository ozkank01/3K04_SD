#utility to view and modify each parameter
from tkinter import ttk
import tkinter as tk

class ParamUtil(tk.Frame):

    def __init__(self,parent,controller,label,r):
        super().__init__(parent)

        self.r = r

        self.paramLabel = ttk.Label(
            self,
            text=label
        ).grid(row=self.r,column=0)

        self.newValue = '0'     #this should be changed to match the value from user's profile

        self.paramVal = ttk.Label(
            self,
            text=self.newValue
        ).grid(row=self.r,column=1)

        self.pButton = ttk.Button(
            self,
            text="Modify",
            command=self.modify()
        ).grid(row=self.r,column=2)
        
        self.newVal = ttk.Entry(
            self,
            textvariable=self.r
        ).grid_remove()

        '''self.valButton = ttk.Button(
            self,
            text="OK",
            command=self.doneModify()
        ).grid_remove()'''

    def modify(self):
        self.newValue = tk.StringVar()
        self.newVal.config(textvariable = self.newValue)
        self.newVal.grid(row=self.r,column=3)
        self.pButton.config(command=self.doneModify())

    #to this function, we need to add something that'll update the new value in the user's profile
    def doneModify(self):
        self.paramVal.config(text=self.newValue)
        self.newVal.grid_remove()
        self.pButton.config(command=self.modify())