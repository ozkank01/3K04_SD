from tkinter import ttk
import tkinter as tk
from functools import partial


class RegisterPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)

        #enter username
        userLabel = ttk.Label(self, text="Username:").grid(row=3,column=0)
        user = tk.StringVar()
        userEntry = ttk.Entry(self, textvariable=user).grid(row=3,column=1)

        #check if username has been taken
        #validate = partial(validateUsername,user)
        userButton = ttk.Button(self,text="Verify Username", command = lambda: controller.newUser()).grid(row=4,column=0,columnspan=2)
        #if username is already in database, run this function again
        #to simplify this, make validateUsername return False if the username is already in database
        self.grid()
