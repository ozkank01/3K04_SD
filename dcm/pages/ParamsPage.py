from tkinter import ttk
import tkinter as tk

class ParamUtil(tk.Frame):

    def __init__(self,parent,controller,label,r):
        super().__init__(parent)

        self.r = r

        self.paramLabel = ttk.Label(self,text=label).grid(row=self.r,column=0)

        self.newValue = '0'     #this should be changed to match the value from user's profile

        self.paramVal = ttk.Label(self,text=self.newValue)
        self.paramVal.grid(row=self.r,column=1)

        self.pButton = ttk.Button(self,text="Modify",command=self.modify())
        
        self.newVal = ttk.Entry(self,textvariable=self.r)

        self.valButton = ttk.Button(self,text="OK",command=self.doneModify())
        
        self.pButton.grid(row=self.r,column=2)


    def modify(self):
        self.pButton.grid_remove()
        self.valButton.grid(row=self.r,column=2)
        self.newValue = tk.StringVar()
        self.newVal.configure(textvariable = self.newValue)
        self.newVal.grid(row=self.r,column=3)

    #to this function, we need to add something that'll update the new value in the user's profile
    def doneModify(self):
        self.pButton.grid(row=self.r,column=2)
        self.valButton.grid_remove()
        self.paramVal.configure(text=self.newValue)
        self.newVal.grid_remove()


class ParamsPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        paramsLabel = ttk.Label(
            self,
            text="View and Modify Parameters"
            ).grid(row=0,column=0,columnspan=2,pady=5)

        self.mode = tk.StringVar(self)
        self.mode.set("AOO")
        
        pacingModes = ttk.OptionMenu(
            self,
            self.mode,
            "AOO", "VOO", "AAI", "VVI"
            )
        #pacingModes.pack()
        pacingModes.grid(row=1,column=0,columnspan=2)

        submitButton = ttk.Button(
            self,
            text="Submit",
            command=self.selectMode()
            )

        toHome = ttk.Button(
            self, 
            text="Return Home",
            style='Accent.TButton' ,
            command=lambda:controller.moveToPage("HomePage")
            ).grid(row=10,column=0)
        
        self.grid()

    def selectMode(self):
        selected = self.mode.get()
        l_r_l = self.createParam(label1="Lower Rate Limit:",r1=1)
        u_r_l = self.createParam(label1="Upper Rate Limit:",r1=2)
        if (self.mode == "AOO"):
            self.modeAOO()
        elif (self.mode == "AAI"):
            self.modeAAI()
        elif (self.mode == "VOO"):
            self.modeVOO()
        else:
            self.modeVVI()
    
    #creates an instance of a parameter to be displayed and modified
    def createParam(self,label1,r1):
        param = ParamUtil(parent=self.parent,controller=self.controller,label=label1,r=r1)
        return param
        
    #Parameters to display:
        #Lower Rate Limit: all
        #Upper Rate Limit: all
        #Atrial Amplitude: AOO, AAI
        #Atrial Pulse Width: AOO, AAI
        #Ventricular Amplitude: VOO, VVI
        #Ventricular Pulse Width: VOO, VVI
        #VRP: VVI
        #ARP: AAI    

    def modeAOO(self):
        at_amp = self.createParam(label1="Atrial Amplitude:",r1=3)
        at_p_w = self.createParam(label1="Atrial Pulse Width:",r1=4)

    def modeAAI(self):
        at_amp = self.createParam(label1="Atrial Amplitude:",r1=3)
        at_p_w = self.createParam(label1="Atrial Pulse Width:",r1=4)
        arp = self.createParam(label1="ARP:",r1=5)

    def modeVOO(self):
        vt_amp = self.createParam(label1="Ventricular Amplitude:",r1=3)
        vt_p_w = self.createParam(label1="Ventricular Pulse Width:",r1=4)

    def modeVVI(self):
        vt_amp = self.createParam(label1="Ventricular Amplitude:",r1=3)
        vt_p_w = self.createParam(label1="Ventricular Pulse Width:",r1=4)
        vrp = self.createParam(label1="VRP:",r1=5)


