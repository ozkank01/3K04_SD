from logging import exception
from re import L
import sqlite3

import sqlite3 as sql


class DataManager():
    def __init__(self):
      self.headers = ('username','password','lowRlimit','uppRLimit','maxSensorRate','fixedAVDelay','dynAVDelay','sensedAVDelayOffset','atrAmp','aPulseW', 'ventAmp','ventPulseW','atSens','ventSens','vRP','aRP','pvaRP','pvaRPExtension','hysterisis','rateSmoothing','atrDur','atrFallMode','atrFallTime','actThresh','reactTime',
      'respFactor','recTime','paceMode', 'pacemakerId')
      self.createTable()


    '''
    PARAMETERS AND THEIR NAMES
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
    hysterisis                  Hysterisis
    rateSmoothing               Rate Smoothing
    atrDur                      ATR Duration
    atrFallMode                 ATR Fallback Mode
    atrFallTime                 ATR Fallback Time
    actThresh                   Activity Threshold
    reactTime                   Reaction Time
    respFactor                  Response Factor
    recTime                     Recovery Time
    '''
      
    
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



