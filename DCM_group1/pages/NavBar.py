from tkinter import ttk
import tkinter as tk


class NavBar(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller =controller
        self.grid(row =0,column =0)
        #goes to Reports page
        self.toReports = ttk.Button(
            self, 
            text="Generate Reports",
            style='Accent.TButton' ,
            command=lambda:self.buttonClick(0)
            )
        self.toReports.grid(row=0,column =0,padx=10,pady=10)

        #goes to Reports page
        self.toParams = ttk.Button(
            self,
            text="View/Modify Parameters",
            style='Accent.TButton',
            command=lambda:self.buttonClick(1)
            )
        self.toParams.grid(row=1,column=0,padx=10,pady=10)
        

        #Log out button
        logoutBtt = ttk.Button(
        self,
        text="Logout",
        style='Accent.TButton',
        command= lambda:self.buttonClick(2)
        )
        logoutBtt.grid(row=2,column =0,pady=10)

       

    def buttonClick(self,butNum):
        if(butNum == 0):
            if(self.controller.getCurrPage()!= "ReportsPage"):
                self.controller.moveToPage("ReportsPage")
        elif(butNum == 1):
            if(self.controller.getCurrPage()!= "ParamsPage"):
                self.controller.moveToPage("ParamsPage")
        elif(butNum == 2):
            self.controller.logout()
