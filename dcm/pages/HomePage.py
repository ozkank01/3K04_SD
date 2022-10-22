from tkinter import ttk
import tkinter as tk
from functools import partial

class HomePage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)

        homeLabel = ttk.Label(self,text="Pacemaker Manager").grid(row=0,column=0,columnspan=2,pady=5)

        #goes to login page
        toReports = ttk.Button(
            self, 
            text="Generate Reports",
            style='Accent.TButton' ,
            command=lambda:controller.moveToPage("ReportsPage")
            ).grid(row=1,column=0)

        #goes to register page
        toParams = ttk.Button(
            self,
            text="View/Modify Parameters",
            style='Accent.TButton',
            command=lambda:controller.moveToPage("ParamsPage")
            ).grid(row=1,column=1)

        self.grid()