from tkinter import ttk
import tkinter as tk

#ParamUtil class: Utility class used to display each parameter to view and modify
class ParamUtil(tk.Frame):

    # label = name of parameter, r = row that this parameter will be displayed in, key = reference in database
    def __init__(self,parent,controller,label,r,key):
        super().__init__(parent)

        # self.r necessary to remove and add widgets to grid
        self.r = r
        # self.key necessary to access and modify values in database
        self.key = key
        self.controller = controller

        # label for parameters
        self.paramLabel = ttk.Label(self,text=label).grid(row=self.r,column=0,padx=5,pady=5,sticky=tk.W)
        # assign displayed value to the current value in user's profile
        self.value = tk.StringVar(self)
        self.vList = self.controller.getValues(self.key)

        # spinbox to enter parameters; values loaded from data manager
        self.entry = ttk.Spinbox(self,values=self.vList,textvariable=self.value,wrap=False)
        self.value.set(self.controller.getPara(self.key))
        self.entry.grid(row=self.r,column=1,padx=5,pady=5)

        #submit button; click to change value in the database
        self.submit = ttk.Button(self,text="OK",command=self.submitF)
        self.submit.grid(row=self.r,column=2,padx=5,pady=5,sticky=tk.W)
        
        self.send = ttk.Button(self,text="YES",command=self.sendF)
        self.cancel = ttk.Button(self,text="NO",command=self.cancelF)
        self.message = ttk.Label(self,text="",foreground="#cf0e25")

    # submitF will check if the new value is within appropriate limits, and if not, will either modify value or cancel
    # the change of parameter (if the software cannot read the value properly)
    def submitF(self):
        val = self.value.get()
        result = self.controller.checkPara(self.key,val)
        msg = ""
        if result == 0:
            msg = "The inputted value " + val + " will be sent to the Pacemaker. Proceed?"
        elif result == 1:
            val = str(self.controller.max(self.key))
            msg = "Inputted value above upper bound. The upper bound " + val + " will be sent to the Pacemaker. Proceed?"
        elif result == 2:
            val = str(self.controller.min(self.key))
            msg = "Inputted value below lower bound. The lower bound " + val + " will be sent to the Pacemaker. Proceed?"
        else:
            msg = "Inputted value cannot be accepted. Value will not be updated."
        self.message.configure(text=msg)
        self.message.grid(row=self.r+1,column=0,columnspan=4,padx=5,pady=5)
        self.cancel.grid(row=self.r+2,column=2,columnspan=2,padx=5,pady=5)
        if result == 3:
            return
        else:
            self.value.set(val)
            self.send.grid(row=self.r+2,column=0,columnspan=2,padx=5,pady=5)

    #this function updates info in database AND sends the value to the pacemaker
    def sendF(self):
        self.message.grid_remove()
        self.cancel.grid_remove()
        self.controller.changePara(self.key,self.value)
        #add a function here that sends the parameter to the Pacemaker using serial communication!!!
        self.send.grid_remove()
    
    #this function cancels the data transmission
    def cancelF(self):
        self.message.grid_remove()
        self.cancel.grid_remove()
        try:
            self.send.grid_remove()
        except:
            return

class ParamsPage(tk.Frame):

    def __init__(self,parent,controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        # window's title
        paramsLabel = ttk.Label(
            self,
            text="View and Modify Parameters"
            ).grid(row=0,column=0,columnspan=5,padx=10,pady=10)
        
        # initialize drop-down menu to AOO. will change this later!
        self.mode = tk.StringVar(self)
        self.initial = self.controller.getPara('paceMode')
        self.mode.set(self.initial)
        self.vals = self.controller.getValues('paceMode')
        
        # drop down menu with pacing modes AOO, AAI, VOO, and VVI
        pacingModes = ttk.OptionMenu(
            self,
            self.mode,
            self.initial,
            *self.vals
            )
        pacingModes.grid(row=1,column=0,columnspan=2,padx=10,pady=10)

        # button will be used to check which parameters should be displayed
        submitButton = ttk.Button(
            self,
            text="Submit",
            command=self.selectMode
            )
        submitButton.grid(row=1,column=2,columnspan=2,padx=10,pady=10)

        # button to return home
        toHome = ttk.Button(
            self, 
            text="Return Home",
            style='Accent.TButton' ,
            command=lambda:controller.moveToPage("HomePage")
            ).grid(row=10,column=0,columnspan=4,padx=10,pady=10)
        
        # creates instances of ParamUtil for ALL parameters. update this list later!
        self.l_r_l = self.createParam(label1="Lower Rate Limit:",r1=3,key1='lowRlimit')
        self.u_r_l = self.createParam(label1="Upper Rate Limit:",r1=4,key1='uppRLimit')
        self.at_amp = self.createParam(label1="Atrial Amplitude:",r1=5,key1='atrAmp')
        self.at_p_w = self.createParam(label1="Atrial Pulse Width:",r1=6,key1='aPulseW')
        self.arp = self.createParam(label1="ARP:",r1=7,key1='aRP')
        self.vt_amp = self.createParam(label1="Ventricular Amplitude:",r1=5,key1='ventAmp')
        self.vt_p_w = self.createParam(label1="Ventricular Pulse Width:",r1=6,key1='ventPulseW')
        self.vrp = self.createParam(label1="VRP:",r1=7,key1='vRP')

        self.grid()

    # selects what to display based on pacing mode chosen
    def selectMode(self):
        selected = self.mode.get()
        # will display lower + upper rate limits NO MATTER what mode is selected
        self.l_r_l.grid()
        self.u_r_l.grid()
        # all mode functions display the required parameters for each mode
        if (selected == "AOO"):
            self.modeAOO()
        elif (selected == "AAI"):
            self.modeAAI()
        elif (selected == "VOO"):
            self.modeVOO()
        else:
            self.modeVVI()
    
    # creates an instance of a parameter to be displayed and modified
    def createParam(self,label1,r1,key1):
        param = ParamUtil(parent=self,controller=self.controller,label=label1,r=r1,key=key1)
        return param
    
    # ALL following functions hide parameters based on pacing mode. Descriptions will contain which parameters should be displayed.
    # Remaining parameters will be HIDDEN!

    # For AOO: Atrial amplitude + atrial pulse width
    def modeAOO(self):
        self.vt_amp.grid_remove()
        self.vt_p_w.grid_remove()
        self.arp.grid_remove()
        self.vrp.grid_remove()
        self.at_amp.grid()
        self.at_p_w.grid()
        
    # For AAI: Atrial amplitude, atrial pulse width + ARP
    def modeAAI(self):
        self.vt_amp.grid_remove()
        self.vt_p_w.grid_remove()
        self.vrp.grid_remove()
        self.at_amp.grid()
        self.at_p_w.grid()
        self.arp.grid()
        
    # For VOO: Ventricular amplitude + ventricular pulse width
    def modeVOO(self):
        self.at_amp.grid_remove()
        self.at_p_w.grid_remove()
        self.arp.grid_remove()
        self.vrp.grid_remove()
        self.vt_amp.grid()
        self.vt_p_w.grid()
        
    # For VVI: Ventricular amplitude, ventricular pulse width + VRP
    def modeVVI(self):
        self.at_amp.grid_remove()
        self.at_p_w.grid_remove()
        self.arp.grid_remove()
        self.vt_amp.grid()
        self.vt_p_w.grid()
        self.vrp.grid()
        

