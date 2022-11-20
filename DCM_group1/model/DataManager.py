from logging import exception
from re import L
import sqlite3

import sqlite3 as sql

    '''
    PARAMETERS AND THEIR KEY NAMES
    lowRlimit                   Lower Rate Limit
    uppRLimit                   Upper Rate Limit
    maxSensorRate               Maximum Sensor Rate
    fixedAVDelay                Fixed AV Delay
    dynAVDelay                  Dynamic AV Delay
    sensedAVDelayOffset         Sensed AV Delay Offset
    atrAmp                      Atrial Amplitude
    aPulseW                     Atrial Pulse Width
    ventAmp                     Ventricular Amplitude
    ventPulseW                  Ventricular Pulse Width
    atSens                      Atrial Sensitivity
    ventSens                    Ventricular Sensitivity
    vRP                         VRP
    aRP                         ARP
    pvaRP                       PVARP
    pvaRPExtension              PVARP Extension
    hysterisis                  Hysterisis0
    rateSmoothing               Rate Smoothing
    atrDur                      ATR Duration
    atrFallMode                 ATR Fallback Mode
    atrFallTime                 ATR Fallback Time
    actThresh                   Activity Threshold
    reactTime                   Reaction Time
    respFactor                  Response Factor
    recTime                     Recovery Time
    '''

class DataManager():
    def __init__(self):
        self.headers = ('username','password','lowRlimit','uppRLimit','maxSensorRate','fixedAVDelay','dynAVDelay','sensedAVDelayOffset','atrAmp','aPulseW', 'ventAmp','ventPulseW','atSens','ventSens','vRP','aRP','pvaRP','pvaRPExtension','hysterisis','rateSmoothing','atrDur','atrFallMode','atrFallTime','actThresh','reactTime',
        'respFactor','recTime','paceMode','pacemakerId')
        self.createTable()
        self.values = {
            'lowRlimit':[], 'uppRLimit':[], 'maxSensorRate':[], 'fixedAVDelay':[],'dynAVDelay':['OFF','ON'], #DONT APPEND
            'sensedAVDelayOffset':['OFF',-10,-20,-30,-40,-50,-60,-70,-80,-90,-100], #DONT APPEND
            'atrAmp':['OFF'], 'aPulseW':['0.05'], 'ventAmp':['OFF'], 'ventPulseW':['0.05'],
            'atSens':['0.25','0.5','0.75'],'ventSens':['0.25','0.5','0.75'],'vRP':[],'aRP':[],'pvaRP':[],'pvaRPExtension':['OFF'],
            'hysterisis':['OFF'],'rateSmoothing':['OFF','3','6','9','12','15','18','21','25'], #DONT APPEND
            'atrDur':['10','20','40','60','80'], 'atrFallMode':['OFF','ON'], #DONT APPEND
            'atrFallTime':[], 'actThresh':['Very Low','Low','Low-Medium','Medium','Medium-High','High','Very High'], #DONT APPEND
            'reactTime':[], 'respFactor':[], 'recTime':[],
            'paceMode':['OFF','DDD','VDD','DDI','DOO','AOO','AAI','VOO','VVI','AAT','VVT','DDDR','VDDR','DDIR','DOOR','AOOR','AAIR','VOOR','VVIR']
        }
        
        self.increments = {
            'uppRLimit':(50,5,175),
            'maxSensorRate':(50,5,175),
            'fixedAVDelay':(70,10,300),
            'aPulseW':(0.1,0.1,1.9),
            'ventPulseW':(0.1,0.1,1.9),
            'atSens':(1.0,0.5,10),
            'ventSens':(1.0,0.5,10),
            'vRP':(150,10,500),
            'aRP':(150,10,500),
            'pvaRP':(150,10,500),
            'pvaRPExtension':(50,50,400),
            'atrDur':(100,100,2000),
            'atrFallTime':(1,1,5),
            'reactTime':(10,10,50),
            'respFactor':(1,1,16),
            'recTime':(2,1,16)
        }
    
        for key in self.values:
            if (key == 'lowRlimit' or key == 'hysterisis'):
                for x in range(30,50,5):
                    self.values[key].append(str(x))
                for x in range(50,90):
                    self.values[key].append(str(x))
                for x in range(90,176,5):
                    self.values[key].append(str(x))
            elif (key == 'atrAmp' or key == 'ventAmp'):
                # Divided by 10 and 2 because step must be INT
                for x in range(5,33):
                    self.values[key].append(str(x/10))
                for x in range(7,15):
                    self.values[key].append(str(x/2))
            elif key in self.increments:
                i = self.increments[key]
                for x in range((i[2]-i[0])/i[1] + 1):
                    self.values[key].append(str(i[0] + x*i[1]))

        self.nominal = {
            'lowRlimit':'60', 'uppRLimit':'120', 'maxSensorRate':'120', 'fixedAVDelay':'150',
            'dynAVDelay':'OFF', 'sensedAVDelayOffset':'OFF', 'atrAmp':'3.5', 'aPulseW':'0.4', 'ventAmp':'3.5', 'ventPulseW':'0.4',
            'atSens':'0.75', 'ventSens':'2.5', 'vRP':'320', 'aRP':'250', 'pvaRP':'250', 'pvaRPExtension':'OFF',
            'hysterisis':'OFF', 'rateSmoothing':'OFF', 'atrDur':'20', 'atrFallMode':'OFF', 'atrFallTime':'1',
            'actThresh':'Medium', 'reactTime':'30', 'respFactor':'8', 'recTime':'5', 'paceMode':'DDD'
        }

    
    #Creates table if there isn't one
    def createTable(self):
        with sql.connect("user.db") as con:
            cur = con.cursor()

            hInputList = [h + " "+ "TEXT," if  h in ('username','password','paceMode','pacemakerId')  else  h + " "+ "REAL," for h in self.headers]
            hInputList[-1] = hInputList[-1][:-1]
            cur.execute("CREATE TABLE IF NOT EXISTS user_data ("+ "".join(hInputList)+")")

    #Adds a user to the table
    def addUser(self, username ='',password ='',lowRlimit =0,uppRLimit =0, atrAmp =0,aPulseW =0, ventAmp =0,ventPulseW =0,vRP =0,aRP =0,paceMode ="", pacemakerId =""):
         with sql.connect("user.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO user_data values (?,?,?,?,?,?,?,?,?,?,?,?)",(username ,password ,lowRlimit ,uppRLimit , atrAmp ,aPulseW , ventAmp ,ventPulseW ,vRP ,aRP,paceMode,pacemakerId ))
    
    #Changes a tuple of values with respect to a tuple of keys 
    def changeVal(self,key,value,username):
        try:
            if not (key in self.headers):
                raise Exception("Invalid key") #done to try to limit  the possibility  of SQL injections since column accessed is variable
            
            with sql.connect("user.db") as con:
                cur = con.cursor()
                
                cur.execute("UPDATE user_data SET "+ key +" =  ? WHERE username = ?",(value,username))
        except Exception as e:
            print(e)
            return
    
    #Checks is if a user is already on the table
    def userExist(self,username):
        with sql.connect("user.db") as con:
            cur = con.cursor()
            cur.execute("SELECT username FROM user_data WHERE username =?",(username,))
            result = cur.fetchone()
            if result:
                return True
            return False
    
    
    #Returns the password for a user in the table
    def getUserPass(self,username):
        with sql.connect("user.db") as con:
            cur = con.cursor()
            cur.execute("SELECT password FROM user_data WHERE username =?",(username,))
            result, = cur.fetchone()
            
            return result
    
    #Returns all user data
    def getUserData(self,username):
        with sql.connect("user.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM user_data WHERE username  =?", (username,))
            result =cur.fetchone()
            return result
    
    #returns a dictionary witn the user data
    def getUserDict(self,username):
        userData =self.getUserData(username)
        return dict(zip(self.headers, userData))

    #Returns the number of users in the database
    def getNumUser(self):
        with sql.connect("user.db") as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(username) FROM user_data")
            result, = cur.fetchone()
            
            return result

    #removes the row from the table with the given user name
    def removeUser(self,username):
        with sql.connect("user.db") as con:
            cur = con.cursor()
            cur.excute("DELETE FROM user_data WHERE username = ?",(username,))

    def getPossValues(self,key):
        return self.values[key]
    



