from tkinter import ttk
import tkinter as tk
from functools import partial

class WelcomePage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        

        welcomeLabel = ttk.Label(self,text="Welcome to Pacemaker Manager!").grid(row=0,column=0,columnspan=2,padx=10,pady=10)

        #goes to login page
        toLogin = ttk.Button(
            self, 
            text="Existing User",
            style='Accent.TButton' ,
            command=lambda:controller.moveToPage("LoginPage")
            ).grid(row=1,column=0,padx=10,pady=15)

        #goes to register page
        toRegister = ttk.Button(
            self,
            text="New User",
            style='Accent.TButton',
            command= controller.toRegPage
            ).grid(row=1,column=1,padx=10,pady=15)
        self.grid()