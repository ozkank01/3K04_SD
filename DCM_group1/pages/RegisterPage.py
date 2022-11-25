from tkinter import ttk
import tkinter as tk
from functools import partial


class RegisterPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.errorLabel = None

        registerLabel = ttk.Label(self,text="Welcome to Pacemaker Manager!").grid(row=0,column=0,columnspan=3,padx=10,pady=10)

        #enter username
        userLabel = ttk.Label(self, text="Username:").grid(row=3,column=0,padx=10,pady=10,sticky="W")
        userEntry = ttk.Entry(self)
        userEntry.grid(row=3,column=1,columnspan=1,padx=10,pady=10)

        #enter password
        passLabel1 = ttk.Label(self, text="Password:").grid(row=4,column=0,padx=10,pady=10,sticky="W")
        passEntry1 = ttk.Entry(self,show='*')
        passEntry1.grid(row=4,column=1,columnspan=2,padx=10,pady=10)
       
        #enter password again
        passLabel2 = ttk.Label(self, text="Confirm Password:").grid(row=5,column=0,padx=5,pady=10,sticky="W") 
        passEntry2 = ttk.Entry(self,show='*')
        passEntry2.grid(row=5,column=1,columnspan=2,padx=10,pady=10)
       

        #calls checkReg to attempt registration
        userButton = ttk.Button(self,text="Enter", command = lambda: self.checkReg(username =userEntry.get(),password = passEntry1.get(), passCheck = passEntry2.get())).grid(row=6,column=0,columnspan=3,padx=10,pady=10)
        self.grid()

    
    #calls registration function and handles incorrect input
    def checkReg(self,username,password,passCheck):
        flag = self.controller.regUser(username=username,password = password, passCheck = passCheck)
        
        #gets rid of error label from previos flag
        if self.errorLabel:
            self.errorLabel.destroy()

        
        #Displays error label based on flag
        if flag == 0:
             # flag is 0, error means user exists.
            self.errorLabel = ttk.Label(self, text="User Exists",foreground="#cf0e25").grid(row=7,column=1,padx=0,pady=10,columnspan=2, sticky="NESW")
        
        elif flag ==-1:
            # flag is -1, error means second entry of password doesn't match
            self.errorLabel = ttk.Label(self, text="Passwords entries do not match",foreground="#cf0e25").grid(row=7,column=1,padx=0,pady=10,columnspan=2, sticky="NESW")

        elif flag ==2:
            # flag is 2, error means username is too short or too long
            self.errorLabel = ttk.Label(self, text="Username must be 4-25 characters in length",foreground="#cf0e25").grid(row=7,column=0,padx=5,pady=10,columnspan=2, sticky="NESW")

        elif flag ==3:
            # flag is 3, error means password is too short or too long
            self.errorLabel = ttk.Label(self, text="Password must be 6-25 characters in length",foreground="#cf0e25").grid(row=7,column=0,padx=5,pady=10,columnspan=2, sticky="NESW")

        elif flag ==4:
            # flag is 4, error means username and/or password contain non-alphanumeric characters
            self.errorLabel = ttk.Label(self, text="Username and password must only contain alphanumeric characters",foreground="#cf0e25").grid(row=7,column=0,padx=5,pady=10,columnspan=2, sticky="NESW")
        
       


                
