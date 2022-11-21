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

        self.entry = ttk.Spinbox(self,values=self.vList,textvariable=self.value,wrap=False)
        self.value.set(self.controller.getPara(self.key))
        self.entry.grid(row=self.r,column=1)
        '''
        # displayed value
        self.displayVal = ttk.Label(self,text=self.value)
        self.displayVal.grid(row=self.r,column=1,padx=5,pady=5,sticky=tk.W)

        # when this button is clicked, a textbox (self.newVal) pops up so you can edit the value
        self.modButton = ttk.Button(self,text="Modify",command=self.modify)
        # textbox to enter new value
        self.newVal = ttk.Entry(self,textvariable=self.r)
        # when this button is clicked, the new value (stored in self.value) is updated in the database
        self.okButton = ttk.Button(self,text="OK",command=self.doneModify)
        
        self.modButton.grid(row=self.r,column=2,padx=5,pady=5,sticky=tk.W)
        '''
    # modify will open the textbox, allowing the user to input a new value
    def modify(self):
        # switch modify button to OK button
        self.modButton.grid_remove()
        self.okButton.grid(row=self.r,column=2,padx=5,pady=5,sticky=tk.W)
        # display textbox
        self.value = tk.IntVar()
        self.newVal.configure(textvariable = self.value)
        self.newVal.grid(row=self.r,column=3,padx=5,pady=5,sticky=tk.W)

    # doneModify will check if the new value is within appropriate limits, and if so, will
    # update the value in the database + close the textbox
    def doneModify(self):
        val = self.value.get()
        # **CHANGE IF STATEMENT TO CHECK IF THE VALUE IS WITHIN LIMITS
        if True:
            # update the value in the database
            self.controller.changePara(self.key,val)
            # switch OK button to modify button
            self.modButton.grid(row=self.r,column=2,padx=5,pady=5,sticky=tk.W)
            self.okButton.grid_remove()
            # display the updated value
            self.displayVal.grid_remove()
            self.displayVal.configure(text=str(val))
            self.displayVal.grid(row=self.r,column=1,sticky=tk.W)
            # remove textbox
            self.newVal.grid_remove()
        else:
            return  # **modify this part to show a pop-up window telling user what the upper and lower limits are + get a diff value


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
        

