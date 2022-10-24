from tkinter import ttk
import tkinter as tk
from functools import partial


class RegisterPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        
        registerLabel = ttk.Label(self,text="Welcome to Pacemaker Manager!").grid(row=0,column=0,columnspan=2,padx=10,pady=10)

        #enter username
        userLabel = ttk.Label(self, text="Username:").grid(row=3,column=0,padx=10,pady=10,sticky="W")
        userEntry = ttk.Entry(self)
        userEntry.grid(row=3,column=1,padx=10,pady=10)

        #enter password
        passLabel1 = ttk.Label(self, text="Password:").grid(row=4,column=0,padx=10,pady=10,sticky="W")
        passEntry1 = ttk.Entry(self,show='*')
        passEntry1.grid(row=4,column=1,padx=10,pady=10)
       
        #enter password again
        passLabel2 = ttk.Label(self, text="Confirm Password:").grid(row=5,column=0,padx=5,pady=10,sticky="W") 
        passEntry2 = ttk.Entry(self,show='*')
        passEntry2.grid(row=5,column=1,padx=10,pady=10)
       

        #check if username has been taken
        #validate = partial(validateUsername,user)
        userButton = ttk.Button(self,text="Enter", command = lambda: controller.regUser(username =userEntry.get(),password = passEntry1.get(), passCheck = passEntry2.get())).grid(row=6,column=0,columnspan=2,padx=10,pady=10)
        #if username is already in database, run this function again
        #to simplify this, make validateUsername return False if the username is already in database
        self.grid()

        # def userButton(self,username,password,passCheck):
        #     flag =controller.regUser(username=username,password = password, passCheck = passCheck)
        #     errLabel = ttk.Label(self,)
        #     if flag ==-1:
                
