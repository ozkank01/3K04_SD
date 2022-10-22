
from shutil import move
import tkinter as tk
from tkinter import ttk

from pages.LoginPage import LoginPage
from pages.WelcomePage import WelcomePage
from pages.RegisterPage import RegisterPage


class DcmController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DCM")
        

        #theme
        style = ttk.Style()
        self.root.tk.call("source", "theme/forest-light.tcl")
        style.theme_use("forest-light")

        #pages active
        self.activePages = {}

        #possible pages
        self.possPages =  {"WelcomePage":WelcomePage,"LoginPage":LoginPage,"RegisterPage":RegisterPage}

        #Updates current page
        self.currPage = tk.Frame()
        self.movePage(pageName="WelcomePage")



    # Starts 
    def dcmRun(self):
        self.root.mainloop()

    #creates an instance of a given page name
    def createPage(self,pageName):
        pageRef = self.possPages[pageName](parent=self.root, controller=self)
        return pageRef

    #moves to given page
    def movePage(self,pageName):
        prevPage = self.currPage
        prevPageName = prevPage.__class__.__name__

        #if pageName is active raises page to the top
        if pageName in self.activePages:
            self.currPage = self.activePages[pageName]
            self.currPage.tkraise()
        else:
            #otherwise creates an instance of page
            self.currPage =self.createPage(pageName=pageName)
            self.activePages[pageName] = self.currPage
            self.currPage.tkraise()
        
        #deletes page if it doesn't need to retain a previous state
        if prevPageName in ("WelcomePage","LoginPage","RegisterPage"):
            self.activePages.pop(prevPageName,None)
            prevPage.destroy()


    #login page logic
    def loginUser(self):
        self.movePage(pageName="LoginPage")

#runs the code
if __name__ == "__main__":
    dcm = DcmController()
    dcm.dcmRun()
