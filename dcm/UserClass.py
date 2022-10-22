from . import Patient
class User:
    username = ""
    password = ""
    
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


    def __init__(self, username, password):
        self.username = username
        self.password = password

    def validate(self, password1):
        return (self.password == password1)



