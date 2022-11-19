from tkinter import ttk
import tkinter as tk
from functools import partial

class WelcomePage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.errorLabel = None
        self.controller = controller

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
            command= self.checkLimReg
            ).grid(row=1,column=1,padx=10,pady=15)
        self.grid()



    #checks if there are 10 users. If not moves to registration page. Otherwise it outpust an error 
    def checkLimReg(self):
        flag = self.controller.toRegPage()

        if self.errorLabel:
            self.errorLabel.destroy()

        # flag is False, then more than 10 users exist
        if not flag:
            self.errorLabel = ttk.Label(self, text="10 Users Exist. User Limit Reached.",foreground="#cf0e25").grid(row=7,column=1,padx=0,pady=10,columnspan=2, sticky="NESW")
        