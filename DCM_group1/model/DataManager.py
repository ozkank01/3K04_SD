from logging import exception
from re import L
import sqlite3

import sqlite3 as sql

class DataManager():
    def __init__(self):
        self.headers = ('username','password','lowRlimit','uppRLimit','atrAmp','aPulseW','ventAmp','ventPulseW','atSens','ventSens','vRP','aRP','paceMode','pacemakerId')
        self.createTable()
        # -1 means OFF
        self.values = {
            'lowRlimit':[], 'uppRLimit':[], 'atrAmp':[-1], 'aPulseW':[], 'ventAmp':[-1], 'ventPulseW':[],
            'atSens':[],'ventSens':[],'vRP':[],'aRP':[],
            'paceMode':['OFF','AOO','AAI','VOO','VVI']
        }
        
        self.increments = {
            'uppRLimit':(50,5,175),
            'atrAmp':(0.1,0.1,5),
            'aPulseW':(1,1,30),
            'ventAmp':(0.1,0.1,5),
            'ventPulseW':(1,1,30),
            'atSens':(0,0.1,5),
            'ventSens':(0,0.1,5),
            'vRP':(150,10,500),
            'aRP':(150,10,500),
        }
       
    
        for key in self.values:
            if (key == 'lowRlimit' or key == 'hysterisis'):
                for x in range(30,50,5):
                    self.values[key].append(str(x))
                for x in range(50,90):
                    self.values[key].append(str(x))
                for x in range(90,176,5):
                    self.values[key].append(str(x))
            elif key in self.increments:
                i = self.increments[key]
                for x in range(int((i[2]-i[0])/i[1] + 1)):
                    self.values[key].append(float(i[0] + x*i[1]))

        self.nominal = {
            'lowRlimit':'60', 'uppRLimit':'120', 'maxSensorRate':'120', 'fixedAVDelay':'150',
            'dynAVDelay':'OFF', 'sensedAVDelayOffset':'OFF', 'atrAmp':'5', 'aPulseW':'1', 'ventAmp':'5', 'ventPulseW':'1',
            'atSens':'0', 'ventSens':'0', 'vRP':'320', 'aRP':'250', 'pvaRP':'250', 'pvaRPExtension':'OFF',
            'hysterisis':'OFF', 'rateSmoothing':'OFF', 'atrDur':'20', 'atrFallMode':'OFF', 'atrFallTime':'1',
            'actThresh':'Medium', 'reactTime':'30', 'respFactor':'8', 'recTime':'5', 'paceMode':'DDD'
        }

    
    #Creates table if there isn't one
    def createTable(self):
        with sql.connect("user.db") as con:
            cur = con.cursor()
            # Either we store certain values ALWAYS as ints OR we have to change this function!!
            hInputList = [h + " "+ "TEXT," if  h in ('username','password','paceMode','pacemakerId')  else  h + " "+ "REAL," for h in self.headers]
            hInputList[-1] = hInputList[-1][:-1]
            cur.execute("CREATE TABLE IF NOT EXISTS user_data ("+ "".join(hInputList)+")")

    #Adds a user to the table
    '''
    def addUser(self,username ='',password ='',pacemakerId =""):
         with sql.connect("user.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO user_data values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(username,password,'60','120','120','150','OFF','OFF','5','1','5','1','0','0','320','250','250','OFF','OFF','OFF','20','OFF','1','Medium','30','8','5','DDD',pacemakerId ))
    '''
    def addUser(self,username ='',password ='',pacemakerId =""):
         with sql.connect("user.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO user_data values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(username,password,60,120,5,1,5,1,0,0,320,250,'AOO',pacemakerId ))

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

    #returns list of possible values for a given key
    def getPossValues(self,key):
        return self.values[key]
    
    #returns minimum value of a given parameter
    def getMin(self,key):
        return self.values[key][0]
    
    #returns maximum value of a given parameter
    def getMax(self,key):
        return self.values[key][len(self.values[key])-1]
    
    #checks if the value is within an acceptable range
    def checkValue(self,key,value):
        v = 0.0
        try:
            v = float(value)
        except:
            #will reset to prev value if cannot convert value to float
            return 3
        if v in self.values[key]:
            #if value is acceptable, say OK
            return 0
        elif v > float(self.values[key][len(self.values[key])-1]):
            #if value is greater than highest value, store as MAX value
            return 1
        elif v < float(self.values[key][0]):
            #if value is smaller than lowest value, store as MIN value
            return 2
        else:
            #otherwise, DO NOT change value! Will be reset back to what it was before submit
            return 3
