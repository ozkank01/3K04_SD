from tkinter import ttk
import tkinter as tk
from functools import partial

class LoginPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller

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
        flag = self.controller.login(username = username, password = password)
        if (flag == False):
            errWindow = tk.Tk()
            errWindow.title("ERROR")
            errText = ttk.Label(errWindow, text='Invalid username and/or password.').grid(column=0,row=0,padx=10,pady=50)

        
