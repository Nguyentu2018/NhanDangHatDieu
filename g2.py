import serial
s = serial.Serial( port=None, baudrate=115200, timeout=0.1)
def open():
    if s.isOpen() == False:
        s.open()
        print('g2 is open')

def send(data):
      s.write((data+"\n").encode('utf-8'))

def read():
     dataRead = s.readline().decode()
     return dataRead

def close():
    if s.isOpen() == True:
        s.close()
        print('g2 is close')

def com(comport):
    s.port = comport
    

