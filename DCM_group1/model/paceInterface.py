#Note: ALL SERIAL COMMUNICATION STUFF WILL GO IN HERE!!!
import serial
import serial.tools.list_ports
import struct
#For some reason, my computer doesn't seem to have any serial ports; I've
#tried to find their names for an hour and it's not working. So make sure to
#put the port name on the line indicated below.

class PaceInterface():
    
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200   #this is taken from tutorial, not sure if ours is the same?
        self.ser.port = 'COM3'
        self.start = b'\x16'    #INITIALIZE serial comm.
        self.sync = b'\x22'     #RECEIVE info from pacemaker
        self.set = b'\x55'      #SEND info to pacemaker

    def sendParams(self,mode,lrl,vPW,vAmp,vSens,vRP,aPW,aAmp,aSens,aRP):
        # DATA SIZES:
        # start (1 byte), set (1 byte), mode (1 byte), LRL (1 byte), vPW (1 byte),
        # vAmp (4 bytes), vSens (4 bytes), vRP (2 bytes), aPW (1 byte), aAmp (4 bytes),
        # aSens (4 bytes), aRP (2 bytes)
        # TOTAL DATA PACKET SIZE: 26 BYTES

        # Pack all values into proper format
        # B = unsigned int, f = float
        mode_s = struct.pack('B', mode)
        lrl_s = struct.pack('B', lrl)
        vPW_s = struct.pack('B', vPW)
        vAmp_s = struct.pack('f', vAmp)
        vSens_s = struct.pack('f', vSens)
        vRP_s = struct.pack('B', vRP)
        aPW_s = struct.pack('B', aPW)
        aAmp_s = struct.pack('f', aAmp)
        aSens_s = struct.pack('f', aSens)
        aRP_s = struct.pack('B', aRP)
        # Pack all 26 bytes together and send serially to the Pacemaker
        sig_set = self.start + self.set + mode_s + lrl_s + vPW_s + vAmp_s + vSens_s + vRP_s + aPW_s + aAmp_s + aSens_s + aRP_s
        self.ser.open()
        self.ser.write(sig_set)

    # used to receive entire packet
    def receiveParams(self):
        data = self.ser.read(22)    # we DO NOT receive the start and sync bytes!
        self.ser.close()
        return data
    
    # will intake the entire data packet and output ONLY the parameter of interest
    def decodeParam(self,data,key):
        #'uppRLimit','atrAmp','aPulseW','atSens','aRP','pacemakerId'
        if (key == 'paceMode'):
            return data[0]
        elif (key == 'lowRlimit'):
            return data[1]
        elif (key == 'ventPulseW'):
            return data[2]
        elif (key == 'ventAmp'):
            return struct.unpack('f', data[3:7])[0]
        elif (key == 'ventSens'):
            return struct.unpack('f', data[7:11])[0]
        elif (key == 'vRP'):
            return data[11]
        elif (key == 'aPulseW'):
            return data[12]
        elif (key == 'atrAmp'):
            return struct.unpack('f', data[13:17])[0]
        elif (key == 'atSens'):
            return struct.unpack('f', data[17:21])[0]
        elif (key == 'aRP'):
            return data[21]
        else:
            return 0

    def changePort(self,port):
        v = 0
        try:
            if self.ser.is_open():
                self.ser.close()
                v = 1
            self.ser.port = port
            if v == 1:
                self.ser.open()
        except:
            print("Port could not be changed.")
    
