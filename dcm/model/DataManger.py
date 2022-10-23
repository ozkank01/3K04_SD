from logging import exception
from re import L
import sqlite3

import sqlite3 as sq
from unittest import result

from numpy import true_divide

class DataManger():
    def __init__(self):
      self.headers = ('username','password','lowRlimit','uppRLimit', 'atrAmp','atrPulseW', 'ventAmp','ventPulseW','vRP','aRP','paceMode')
      self.createTable()

      
       
    def dataConnect(self):
        self.con = sq.connect("user.db")
        self.cursor = self.con
    
    def dataQuit(self):
       self.con.close()
    
    def createTable(self):
        with sq.connect("user.db") as con:
            cur = con.cursor()

            hInputList = [h + " "+ "TEXT," if  h in ('username','password','paceMode')  else  h + " "+ "REAL," for h in self.headers]
            cur.execute("CREATE TABLE IF NOT EXISTS user_data (?,?,?,?,?,?,?,?,?,?,?)", hInputList)
        

    def addUser(self, username ='',password ='',lowRlimit =0,uppRLimit =0, atrAmp =0,atrPulseW =0, ventAmp =0,ventPulseW =0,vRP =0,aRP =0,paceMode =""):
         with sq.connect("user.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO user_data values (?,?,?,?,?,?,?,?,?,?,?)",(username ,password ,lowRlimit ,uppRLimit , atrAmp ,atrPulseW , ventAmp ,ventPulseW ,vRP ,aRP,paceMode))
    
    def changeVal(self,keys,values,username):
        try:
            if not(set(keys).issubset(self.headers)):
                raise Exception("Invalid keys")
            elif len(set(keys)) != len(keys):
                raise Exception("Repeating keys")
            elif len(keys) != len(values):
                raise Exception("Mismatch between number of keys and number values")
            
            with sq.connect("user.db") as con:
                cur = con.cursor()
                temp = "("+"?,"*(len(keys)-1)+"?"+")"
                cur.execute("UPDATE user_data SET ("+",".join(keys) + ") = " + temp,values)
        except Exception as e:
            print(e)
            return
    
    def userExist(self,username):
        with sq.connect("user.db") as con:
            cur = con.cursor()
            cur.execute("SELECT username FROM user_data WHERE username =?",username)
            result = cur.fetchone()
            if result:
                return True
            return False
    
    def getUserPass(self,username):
        with sq.connect("user.db") as con:
            cur = con.cursor()
            cur.execute("SELECT password FROM user_data WHERE username =?",username)
            result = cur.fetchone()
            return result
    
    def getUserData(self,username):
        with sq.connect("user.db") as con:
            cur = con.cursor()
            cur.excute("SELECT * FROM user_data WHERE username  =?", username)


