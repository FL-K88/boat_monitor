## to find current ports: portData = serial.tools.list_ports.comports() OR python -m serial.tools.list_ports
import datetime
import time
import serial
from multiprocessing import Process

ser = [serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 10)] ##[Leonardo]
logData = []
def readData(selector):
    while 1:
        arduinoData = ser[selector].readline().decode('ascii')
        ##Store data by timestamp
        data = [datetime.datetime.now(), arduinoData]

        ##drop the earliest element if more than a year's worth of data is stored
        if len(logData) > (24*366):
            del logData[0]

        logData.append(data)
        print(logData[-1])
        time.sleep(5) ##ultimately change to 3600 (1 hour)
        

if __name__ == '__main__':
    leo = Process(target = readData, args=(0,))
    leo.start()
    leo.join()