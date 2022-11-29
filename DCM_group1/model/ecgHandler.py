import serial
import serial.tools.list_ports
import struct

class ECGHandler():
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200   #this is taken from tutorial, not sure if ours is the same?
        self.ser.port = 'COM3'
        self.req = b'\x47'      #send REQUEST to receive ECG data
        self.sync = b'\x16'     #is at the start of any data packet
        self.stop = b'\x62'     #STOP ecg transmission

    def ecgStart(self):
        # This packet is n + 3 bytes large (n = 13, so 16 bytes)
        e = struct.pack('B',0)      #not transmitting anything except for "start streaming" signal
        sig_set = self.sync + self.req + e + e + e + e + e + e + e + e + e + e + e + e + e + e #final e is checksum; sum is 0
        self.ser.open()
        self.ser.write(sig_set)

    def ecgStop(self):
        e = struct.pack('B',0)      #not transmitting anything except for "start streaming" signal
        sig_set = self.sync + self.stop + e + e + e + e + e + e + e + e + e + e + e + e + e + e #final e is checksum; sum is 0
        self.ser.write(sig_set)
        self.ser.close()

    def ecgRead(self):
        #ecg streams 4 BYTES AT A TIME
        data = self.ser.read(4)
        return data

    def ecgDecode(self,data,k):
        if k == 0:
            return struct.unpack('H', data[0:2])[0] #will return the m_vraw reading
        else:
            return struct.unpack('H', data[2:4])[0] #will return the f_marker reading3