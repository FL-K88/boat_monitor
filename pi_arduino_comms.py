## to find current ports: portData = serial.tools.list_ports.comports()
import datetime
import serial
from multiprocessing import Process

ser = [serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 10)] ##[Leonardo]
logData = []

##generate timestamp for data point, then store by hash of mm/yyyy?

def readData(selector):
    while 1:
        arduinoData = ser[selector].readline().decode('ascii')
        ##Store data by timestamp
        data = [datetime.datetime.now(), arduinoData]
        logData.append(data)
        print(logData[-1])
        

if __name__ == '__main__':
    leo = Process(target = readData, args=(0,))
    leo.start()
    leo.join()