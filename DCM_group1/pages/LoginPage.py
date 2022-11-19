from tkinter import ttk
import tkinter as tk
from functools import partial

class LoginPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.errorLabel =None

        loginLabel = ttk.Label(self,text="Welcome to Pacemaker Manager!").grid(row=0,column=0,columnspan=2,padx=10,pady=10)
        
        #enter username
        userLabel = ttk.Label(self, text="Username:").grid(row=3,column=0,padx=10,pady=10,sticky="W")
        userEntry = ttk.Entry(self)
        userEntry.grid(row=3,column=1,padx=10,pady=10)

        #enter password
        passLabel = ttk.Label(self, text="Password:").grid(row=4,column=0,padx=10,pady=10,sticky="W")
        password =tk.StringVar()
        passEntry = ttk.Entry(self,show='*')
        passEntry.grid(row=4,column=1,padx=10,pady=10)
       
        
        loginButton = ttk.Button(self, text="Login", command= lambda: self.checkLogin(username =userEntry.get(),password = passEntry.get())).grid(row=5,column=0,columnspan=2,padx=10,pady=10)
        self.grid()

    def checkLogin(self,username,password):
        flag = self.controller.login(username=username,password = password)

        if self.errorLabel:
            self.errorLabel.destroy()

        # flag is 0 error means user exists
        if flag == 0:
            self.errorLabel = ttk.Label(self, text="User Does Not Exist",foreground="#cf0e25").grid(row=7,column=1,padx=0,pady=10,columnspan=2, sticky="NESW")
        
        # flag is 1 error means second entry of password doesn't match
        elif flag ==-1:

            self.errorLabel = ttk.Label(self, text="Incorrect Password",foreground="#cf0e25").grid(row=7,column=1,padx=0,pady=10,columnspan=2, sticky="NESW")

        
