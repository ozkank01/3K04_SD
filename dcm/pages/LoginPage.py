from tkinter import ttk
import tkinter as tk
from functools import partial

class LoginPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        

        

        #enter username
        userLabel = ttk.Label(self, text="Username:").grid(row=3,column=0)
        username = tk.StringVar()
        userEntry = ttk.Entry(self, textvariable=username).grid(row=3,column=1)

        #enter password
        passLabel = ttk.Label(self, text="Password:").grid(row=4,column=0)
        password = tk.StringVar()
        passEntry = ttk.Entry(self, textvariable=password,show="*").grid(row=4,column=1)

        #validate = partial(validateLogin, user, password)
        loginButton = ttk.Button(self, text="Login", command= lambda: self.controller.login(username =username,password =password)).grid(row=5,column=0,columnspan=2)

        self.grid()