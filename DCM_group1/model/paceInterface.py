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
        #self.ser.port = <REPLACE THIS WITH SERIAL PORT NAME!>
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
        # B = unsigned int, f = float, H = unsigned short
        vRP_t = (vRP - 150)/10
        aRP_t = (aRP - 150)/10
        
        mode_s = struct.pack('B', mode)
        lrl_s = struct.pack('B', lrl)
        vPW_s = struct.pack('B', vPW)
        vAmp_s = struct.pack('f', vAmp)
        vSens_s = struct.pack('f', vSens)
        vRP_s = struct.pack('B', vRP_t)
        vRP_s = struct.pack('B', int(vRP_t))
        aPW_s = struct.pack('B', aPW)
        aAmp_s = struct.pack('f', aAmp)
        aSens_s = struct.pack('f', aSens)
        aRP_s = struct.pack('B', aRP_t)
        aRP_s = struct.pack('B', int(aRP_t))
        # Pack all 26 bytes together and send serially to the Pacemaker
        sig_set = self.start + self.set + mode_s + lrl_s + vPW_s + vAmp_s + vSens_s + vRP_s + aPW_s + aAmp_s + aSens_s + aRP_s
        self.ser.write(sig_set)

    # used to receive entire packet
    def receiveParams(self):
        data = self.ser.read(24)    # we DO NOT receive the start and sync bytes!
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
            return struct.unpack('H', data[11:13])[0]
        elif (key == 'aPulseW'):
            return data[13]
        elif (key == 'atrAmp'):
            return struct.unpack('f', data[14:18])[0]
        elif (key == 'atSens'):
            return struct.unpack('f', data[18:22])[0]
        elif (key == 'aRP'):
            return struct.unpack('H', data[22:24])[0]
        else:
            return 0
    
a = PaceInterface()