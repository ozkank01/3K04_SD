
from logging import root
from pickle import FALSE
import tkinter as tk
from tkinter import ttk

from numpy import true_divide

from model.DataManager import DataManager
from model.UserClass import User

from pages.LoginPage import LoginPage
from pages.WelcomePage import WelcomePage
from pages.RegisterPage import RegisterPage
from pages.HomePage import HomePage
from pages.ReportsPage import ReportsPage
from pages.ParamsPage import ParamsPage


class DcmController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DCM")
        self.currUser = None
        self.dataManager = DataManager()

        self.container = tk.Frame(self.root)
        self.container.grid()
        #theme
        style = ttk.Style()
        self.root.tk.call("source", "theme/forest-light.tcl")
        style.theme_use("forest-light")

        #pages active
        self.activePages = {}

        #possible pages
        self.possPages =  {"WelcomePage":WelcomePage,"LoginPage":LoginPage,"RegisterPage":RegisterPage,"HomePage":HomePage,"ReportsPage":ReportsPage,"ParamsPage":ParamsPage}

        #Updates current page
        self.currPage = tk.Frame()
        self.moveToPage("WelcomePage")



    # Starts 
    def dcmRun(self):
        self.root.mainloop()

    #creates an instance of a given page name
    def createPage(self,pageName):
        pageRef = self.possPages[pageName](parent=self.container, controller=self)
        return pageRef

    #moves to given page
    def moveToPage(self,pageName):
        prevPage = self.currPage
        prevPageName = prevPage.__class__.__name__

        #if pageName is active raises page to the top
        if pageName in self.activePages:
            self.currPage = self.activePages[pageName]
            self.currPage.tkraise()
            self.currPage.grid() #if page was active before the function call, it must have been a prevoius page that was .grid_removed

        else:
            #otherwise creates an instance of page an raises it to the top
            self.currPage =self.createPage(pageName=pageName)
            self.activePages[pageName] = self.currPage
            self.currPage.tkraise()
        

        #deletes page if it doesn't need to retain a previous state
        if prevPageName in ("WelcomePage","LoginPage","RegisterPage","HomePage","ParamsPage"):
            self.activePages.pop(prevPageName,None)
            prevPage.destroy()

        #Otherwise it hides the widgets
        else:
            prevPage.grid_remove()
    



    #login page logic
    def login(self,username,password):            
            if self.dataManager.userExist(username) and (self.dataManager.getUserPass(username) ==password):
                self.moveToPage("HomePage")
                self.currUser = self.dataManager.getUserDict(username)
                return True
            
            return False
        
    
    #registor page logic
    def toRegPage(self):
        if(self.dataManager.getNumUser() < 10):       
            self.moveToPage("RegisterPage")
            return True
        return False
            

    
    def regUser(self,username,password, passCheck):
       
        if(password != passCheck):
            return -1
        
        elif not self.dataManager.userExist(username):
            self.dataManager.addUser(username=username, password=password)
            self.moveToPage("HomePage")
            self.currUser = self.dataManager.getUserDict(username)

            return 1
        return 0
    
    #Logic after Login
    def diffPaceMaker(self,pacemakerId):
        return self.currUser["pacemakerId"] ==pacemakerId
    
    #gets data from user
    def getPara(self, key):
        return self.currUser[key]
    
    #changes data for user
    def changePara(self,key, value):
        self.currUser[key] = val
        self.dataManager.changeVal(key = key, value = value,username = self.currUser['username'] )

   



#runs the code
if __name__ == "__main__":
    dcm = DcmController()
    dcm.dcmRun()
