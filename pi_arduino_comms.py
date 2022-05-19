## to find current ports: portData = serial.tools.list_ports.comports()

import serial
from multiprocessing import Process

ser = [serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 10)] ##[Leonardo]

def readData(selector):
    while 1:
        arduinoData = ser[selector].readline().decode('ascii')
        print(arduinoData)
        

if __name__ == '__main__':
    leo = Process(target = readData, args=(0,))
    ##uno = Process(target = readData, args=(1,))
    ##uno.start()
    leo.start()
    ##uno.join()
    leo.join()