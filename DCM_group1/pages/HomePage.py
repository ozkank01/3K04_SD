from tkinter import ttk
import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)

        homeLabel = ttk.Label(self,text="Pacemaker Manager").grid(row=0,column=0,columnspan=2,padx=10,pady=10)

        #goes to Reports page
        self.toReports = ttk.Button(
            self, 
            text="Generate Reports",
            style='Accent.TButton' ,
            command=lambda:controller.moveToPage("ReportsPage")
            )
        self.toReports.grid(row=1,column=0,padx=10,pady=15)

        #goes to Reports page
        self.toParams = ttk.Button(
            self,
            text="View/Modify Parameters",
            style='Accent.TButton',
            command=lambda:controller.moveToPage("ParamsPage")
            )
        self.toParams.grid(row=1,column=1,padx=10,pady=15)
        self.grid()
