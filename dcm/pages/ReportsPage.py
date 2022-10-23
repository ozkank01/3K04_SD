from tkinter import ttk
import tkinter as tk

class ReportsPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        
        reportsLabel = ttk.Label(
            self,
            text="This page will be used to generate reports!"
            ).grid(row=0,column=0,columnspan=2,pady=5)
        
        toHome = ttk.Button(
            self, 
            text="Return Home",
            style='Accent.TButton' ,
            command=lambda:controller.moveToPage("HomePage")
            ).grid(row=10,column=0)