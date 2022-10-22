from . import Patient
class User:
    name = ""
    username = ""
    password = ""
    patientList = []
    
    lRLimit =0
    uRLimit =0
    artAmp =0
    artPulseW = 0
    ventAmp =0
    ventPulseW =0
    vRP =0
    aRP =0
    paceConnect = 0
    pacePos =0
    paceId =""


    def __init__(self,name, username, password):
        self.name  =name
        self.username = username
        self.password = password



