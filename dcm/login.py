from tkinter import ttk
import tkinter
from functools import partial

#utility function to HIDE widgets
def remove(widget):
    widget.grid_remove()

#utility function to SHOW widgets
def display(widget,r,c,cs):
    widget.grid(row=r,column=c,columnspan=cs)

#declare all widgets HERE

#NOTE: We need a way for this program to handle outputs from functions associated with button presses!
#Modify this function to check that username matches password
def validateLogin(user,password):
    print("Username Entered:", user.get())
    print("Password Entered:", password.get())
    return

#Modify this function to check that password1 == password2
def validatePassword(password1,password2):
    print("Password Entered:",password1.get())
    print("Repeat Entry:",password2.get())
    #return False if passwords do not match, meaning passEnter repeats itself
    return

def passEnter():
    #enter password
    passLabel1 = ttk.Label(welcome, text="Password:").grid(row=4,column=0)
    password1 = tkinter.StringVar()
    passEntry1 = ttk.Entry(welcome, textvariable=password1,show="*").grid(row=4,column=1)

    #verify password
    passLabel2 = ttk.Label(welcome, text="Verify Password:").grid(row=5,column=0)
    password2 = tkinter.StringVar()
    passEntry2 = ttk.Entry(welcome, textvariable=password2,show="*").grid(row=5,column=1)

    validate = partial(validatePassword,password1,password2)
    passButton = ttk.Button(welcome,text="Verify Password",command=validate).grid(row=6,column=0,columnspan=2)

#Modify this function to check that username is not already in database
def validateUsername(user):
    print("Username Entered:",user.get())
    #if username is already in database: registerUser()
    #add username to database HERE
    passEnter()

def loginUser():
    welcome.geometry("400x400")

    #enter username
    userLabel = ttk.Label(welcome, text="Username:").grid(row=3,column=0)
    user = tkinter.StringVar()
    userEntry = ttk.Entry(welcome, textvariable=user).grid(row=3,column=1)

    #enter password
    passLabel = ttk.Label(welcome, text="Password:").grid(row=4,column=0)
    password = tkinter.StringVar()
    passEntry = ttk.Entry(welcome, textvariable=password,show="*").grid(row=4,column=1)

    validate = partial(validateLogin, user, password)
    loginButton = ttk.Button(welcome, text="Login",command=validate).grid(row=5,column=0,columnspan=2)


def registerUser():
    welcome.geometry("400x400")

    #enter username
    userLabel = ttk.Label(welcome, text="Username:").grid(row=3,column=0)
    user = tkinter.StringVar()
    userEntry = ttk.Entry(welcome, textvariable=user).grid(row=3,column=1)

    #check if username has been taken
    validate = partial(validateUsername,user)
    userButton = ttk.Button(welcome,text="Verify Username",command=validate).grid(row=4,column=0,columnspan=2)
    #if username is already in database, run this function again
    #to simplify this, make validateUsername return False if the username is already in database

#base window - customize appearance!
welcome = tkinter.Tk()
style = ttk.Style()
style.configure('.', padding=6,background='white',font=('Calibri',12))
welcome.geometry("400x150")
welcome.title("Welcome to Pacemaker Manager!")

welcomeLabel = ttk.Label(welcome,text="Welcome to Pacemaker Manager!").grid(row=0,column=0,columnspan=2,pady=5)
login = ttk.Button(welcome, text="Existing User",command=loginUser).grid(row=1,column=0)
register = ttk.Button(welcome, text="New User",command=registerUser).grid(row=1,column=1)

welcome.mainloop()