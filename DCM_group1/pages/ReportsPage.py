from tkinter import ttk
import tkinter as tk

class ReportsPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        
        reportsLabel = ttk.Label(
            self,
            text="This page will be used to generate reports!"
            ).grid(row=1,column=0,columnspan=2,padx=10,pady=10)
        
        toHome = ttk.Button(
            self, 
            text="Return Home",
            style='Accent.TButton' ,
            command=lambda:controller.moveToPage("HomePage")
            ).grid(row=10,column=0,columnspan=2,padx=10,pady=10)
        self.grid()

'''
AVAILABLE REPORTS
Bradycardia Parameters: Programmable parameters for selected pacing mode
Electrogram Report: Atrial + ventricular lead data from pacemaker

Each report MUST contain the following header info:
- Institution name (McMaster University?)
- Date and time of report printing (RTC?)
- Device model and serial number
- DCM serial number
- Application model and version number
- Report name
'''        