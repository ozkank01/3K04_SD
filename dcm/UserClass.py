from . import Patient
class User:
    username = ""
    password = ""
    
    lowRLimit =0
    uppRLimit =0
    atrAmp =0
    atrPulseW = 0
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



