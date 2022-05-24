## to find current ports: portData = serial.tools.list_ports.comports() OR python -m serial.tools.list_ports
import datetime
import time
import serial
from multiprocessing import Process
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

ser = [serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 10)] ##[Leonardo]
logData = []
def readData(selector):
    while 1:
        arduinoData = ser[selector].readline().decode('ascii')
        arduinoData = float(arduinoData.strip("\r\n"))
        ##Store data by timestamp
        data = [datetime.datetime.now(), arduinoData]

        ##drop the earliest element if more than a year's worth of data is stored
        if len(logData) > (24*366):
            del logData[0]

        logData.append(data)
        print(logData[-1])
        if len(logData) > 23:
            dailyPlot(logData)
            exit()
        time.sleep(1) ##ultimately change to 3600 (1 hour)

def dailyPlot(logData):
    sl = slice(-24,-1) 
    data = np.array(logData[sl])
    np.append(data,logData[-1]) ##accounts for slice not including final element
    #print(data[0][0])
    #print(data[-1][0])
    maxDate = data[0][0] ##assumes logData is ordered with first element earliest
    minDate = data[-1][0]
    ##print(minDate.strftime('%Y-%m-%d'))
    ##print(maxDate.strftime('%Y-%m-%d'))
    x = data[:,0].astype(datetime.datetime.strftime('%Y-%m-%d'))
    y = data[:,1]
    print("x:", x)
    print("y:", y)
    plt.plot(x,y,linewidth=2.0)
    ##plt.set(xlim=(0, 8), xticks=np.arange(1, 8),
    ##   ylim=(0, 8), yticks=np.arange(1, 8))
    plt.show() 

if __name__ == '__main__':
    leo = Process(target = readData, args=(0,))
    leo.start()
    leo.join()