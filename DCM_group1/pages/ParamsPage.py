from tkinter import ttk
import tkinter as tk

class ParamUtil(tk.Frame):

    def __init__(self,parent,controller,label,r,key):
        super().__init__(parent)

        self.r = r
        self.key = key
        self.controller = controller

        self.paramLabel = ttk.Label(self,text=label).grid(row=self.r,column=0,padx=5,pady=5,sticky=tk.W)

        self.newValue = self.controller.getPara(self.key)     #this should be changed to match the value from user's profile

        self.paramVal = ttk.Label(self,text=self.newValue)
        self.paramVal.grid(row=self.r,column=1,padx=5,pady=5,sticky=tk.W)

        self.pButton = ttk.Button(self,text="Modify",command=self.modify)
        
        self.newVal = ttk.Entry(self,textvariable=self.r)

        self.valButton = ttk.Button(self,text="OK",command=self.doneModify)
        
        self.pButton.grid(row=self.r,column=2,padx=5,pady=5,sticky=tk.W)


    def modify(self):
        self.pButton.grid_remove()
        self.valButton.grid(row=self.r,column=2,padx=5,pady=5,sticky=tk.W)
        self.newValue = tk.IntVar()
        self.newVal.configure(textvariable = self.newValue)
        self.newVal.grid(row=self.r,column=3,padx=5,pady=5,sticky=tk.W)

    #to this function, we need to add something that'll update the new value in the user's profile
    def doneModify(self):
        val = self.newValue.get()
        self.controller.changePara(self.key,val)
        self.pButton.grid(row=self.r,column=2,padx=5,pady=5,sticky=tk.W)
        self.valButton.grid_remove()
        self.paramVal.grid_remove()
        self.paramVal.configure(text=str(val))
        self.paramVal.grid(row=self.r,column=1,sticky=tk.W)
        self.newVal.grid_remove()


class ParamsPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        paramsLabel = ttk.Label(
            self,
            text="View and Modify Parameters"
            ).grid(row=0,column=0,columnspan=5,padx=10,pady=10)
        
        self.mode = tk.StringVar(self)
        self.mode.set("AOO")
        
        #drop down menu with pacing modes
        pacingModes = ttk.OptionMenu(
            self,
            self.mode,
            "AOO",
            "AOO", "AAI", "VOO", "VVI"
            )
        pacingModes.grid(row=1,column=0,columnspan=2,padx=10,pady=10)

        submitButton = ttk.Button(
            self,
            text="Submit",
            command=self.selectMode
            )

        submitButton.grid(row=1,column=2,columnspan=2,padx=10,pady=10)

        toHome = ttk.Button(
            self, 
            text="Return Home",
            style='Accent.TButton' ,
            command=lambda:controller.moveToPage("HomePage")
            ).grid(row=10,column=0,columnspan=4,padx=10,pady=10)
        
        #creates instances of ParamUtil for parameters
        self.l_r_l = self.createParam(label1="Lower Rate Limit:",r1=3,key1='lowRlimit')
        self.u_r_l = self.createParam(label1="Upper Rate Limit:",r1=4,key1='uppRLimit')
        self.at_amp = self.createParam(label1="Atrial Amplitude:",r1=5,key1='atrAmp')
        self.at_p_w = self.createParam(label1="Atrial Pulse Width:",r1=6,key1='aPulseW')
        self.arp = self.createParam(label1="ARP:",r1=7,key1='aRP')
        self.vt_amp = self.createParam(label1="Ventricular Amplitude:",r1=5,key1='ventAmp')
        self.vt_p_w = self.createParam(label1="Ventricular Pulse Width:",r1=6,key1='ventPulseW')
        self.vrp = self.createParam(label1="VRP:",r1=7,key1='vRP')

        self.grid()

    #Selects what to display based on pacing mode chosen
    def selectMode(self):
        selected = self.mode.get()
        self.l_r_l.grid()
        self.u_r_l.grid()
        if (selected == "AOO"):
            self.modeAOO()
        elif (selected == "AAI"):
            self.modeAAI()
        elif (selected == "VOO"):
            self.modeVOO()
        else:
            self.modeVVI()
    
    #creates an instance of a parameter to be displayed and modified
    def createParam(self,label1,r1,key1):
        param = ParamUtil(parent=self,controller=self.controller,label=label1,r=r1,key=key1)
        return param
    
    #Functions that hide parameters based on pacing mode
    def modeAOO(self):
        self.vt_amp.grid_remove()
        self.vt_p_w.grid_remove()
        self.arp.grid_remove()
        self.vrp.grid_remove()
        self.at_amp.grid()
        self.at_p_w.grid()
        

    def modeAAI(self):
        self.vt_amp.grid_remove()
        self.vt_p_w.grid_remove()
        self.vrp.grid_remove()
        self.at_amp.grid()
        self.at_p_w.grid()
        self.arp.grid()
        

    def modeVOO(self):
        self.at_amp.grid_remove()
        self.at_p_w.grid_remove()
        self.arp.grid_remove()
        self.vrp.grid_remove()
        self.vt_amp.grid()
        self.vt_p_w.grid()
        

    def modeVVI(self):
        self.at_amp.grid_remove()
        self.at_p_w.grid_remove()
        self.arp.grid_remove()
        self.vt_amp.grid()
        self.vt_p_w.grid()
        self.vrp.grid()
        

