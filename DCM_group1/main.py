
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
        

        #container for pages
        self.container = tk.Frame(self.root)
        self.container.grid()
        #theme
        style = ttk.Style()
        self.root.tk.call("source", "theme/forest-light.tcl")
        style.theme_use("forest-light")

        #bottom bar frame
        self.bttmBar =tk.Frame(self.root)

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

        if self.currUser:
            print(5)
            #progressbar displays current connection status
            connect = ttk.Progressbar(self.bttmBar,orient='horizontal',mode='indeterminate',length=200)
            connect.grid(column=0,row=0,columnspan=5,padx=10,pady=5)
            connect.start()  #initialized as disconnected


            #label displays current connection status in words
            connectLabel = ttk.Label(self.bttmBar,text='Connecting to Pacemaker...',)
            connectLabel.grid(column=0,row=1,columnspan=5,padx=20,pady=10)

            #Log out button
            logoutBtt = ttk.Button(
            self.bttmBar,
            text="Logout",
            style='Accent.TButton',
            command= self.logout
            )
            logoutBtt.grid(column=5,row=1,rowspan= 2,sticky='NW')

            self.bttmBar.grid()
    

    #-------------Bottom Bar Logic---------------
    def logout(self):
        self.currUser =None
        self.moveToPage("WelcomePage")
        self.bttmBar.grid_remove()

    #-------------login page logic---------------

    #logs in an existing user
    def login(self,username,password):            
            if not self.dataManager.userExist(username):
                
                return 0
            elif  not (self.dataManager.getUserPass(username) ==password):
                return -1 
            
            self.currUser = self.dataManager.getUserDict(username)
            self.moveToPage("HomePage")
            return 1
        
    
    #------------Register page logic----------------

    #moves to Register page
    def toRegPage(self):
        if(self.dataManager.getNumUser() < 10):       
            self.moveToPage("RegisterPage")
            return True
        return False
            

    #
    def regUser(self,username,password, passCheck):
       
        if self.dataManager.userExist(username):
            #User exists already
            return 0
       
        elif(password != passCheck):
            #second entry of password doesn't match
            return -1
        
        elif(len(username) < 4 or len(username) > 25):
            #will not allow usernames to be shorter than 4 characters or longer than 25 characters
            return 2
        
        elif (len(password) < 6 or len(password) > 25):
            #will not allow passwords to be shorter than 6 characters or longer than 25 characters
            return 3

        elif username.isalnum() == False or password.isalnum() == False:
            #will not allow usernames/passwords to contain non-alphanumeric characters
            return 4
        
        #registers accepted input
        self.dataManager.addUser(username=username, password=password)
        self.moveToPage("HomePage")
        self.currUser = self.dataManager.getUserDict(username)
        return 1
        
    
    #********User specific functions(after logging in)**********
    def diffPaceMaker(self,pacemakerId):
        return self.currUser["pacemakerId"] ==pacemakerId
    
    #gets data from user
    def getPara(self, key):
        return self.currUser[key]
    
    #changes data for user
    def changePara(self,key, value):
        self.currUser[key] = value
        self.dataManager.changeVal(key = key, value = value,username = self.currUser['username'] )
    
    #gets list of values for spinbox (ParamsPage)
    def getValues(self,key):
        return self.dataManager.getPossValues(key)

    #will be called once pacemaker is considered connected
    def connected(self):
        if (self.currUser != None):
            self.connect.stop()
            self.connectLabel.grid_remove()
            self.connectLabel.configure(text='Connected to Pacemaker!')
            self.connectLabel.grid(column=0,row=21,columnspan=5,padx=20,pady=10)

    #will be called once pacemaker is considered disconnected 
    def disconnected(self):
        if (self.currUser != None):
            self.connect.start()
            self.connectLabel.grid_remove()
            self.connectLabel.configure(text='Connecting to Pacemaker...')
            self.connectLabel.grid(column=0,row=21,columnspan=5,padx=20,pady=10)

    #note: we still have to work out the internal logic to determine whether the pacemaker is connected or not!

    # used to check if a parameter is valid
    def checkPara(self,key,value):
        return self.dataManager.checkValue(key,value)
    
    def min(self,key):
        return self.dataManager.getMin(key)

    def max(self,key):
        return self.dataManager.getMax(key)



#runs the code
if __name__ == "__main__":
    dcm = DcmController()
    dcm.dcmRun()
