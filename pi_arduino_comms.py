## to find current ports: portData = serial.tools.list_ports.comports() OR python -m serial.tools.list_ports
import datetime
import time
import serial
from multiprocessing import Process
import matplotlib
from matplotlib import pyplot as plt
import numpy as np


ser = [serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 10)] ##[Arduino Leonardo]
logData = []
def readData(selector):
    while 1:
        ##arduino transmits 1 voltage reading per second to the pi.
        arduinoData = ser[selector].readline().decode('ascii')
        arduinoData = float(arduinoData.strip("\r\n"))

        if isinstance(arduinoData,float) == False:
            print("voltage stored as " + str(type(arduinoData)) + ", not float")
        
        ##Store data by timestamp
        data = [datetime.datetime.now(), arduinoData]

        ##drop the earliest element if more than a year's worth of data is stored
        if len(logData) > (24*366):
            del logData[0]

        logData.append(data)
        print(logData[-1]) ## print datapoint just added
        if len(logData) > 23:
            dailyPlot(logData)
            exit()
        time.sleep(1) ##ultimately change to 3600/1 hour

def dailyPlot(logData):
    sl = slice(-24,-1) 
    data = logData[sl]
    data.append(logData[-1]) ##accounts for slice not including final element
    maxDate = data[0][0] ##assumes logData is ordered with first element earliest
    minDate = data[-1][0]

    ## print(minDate.strftime('%Y-%m-%d'))
    ## print(maxDate.strftime('%Y-%m-%d'))
    x = np.arange(start=0,stop=24,step=1) ## time offset. Temporary. Insures chart is getting only ints and floats
    y = np.asarray(data)[:,1]
    if not isinstance(x, list):
        x = x.tolist()
    if not isinstance(y, list):
        y = y.tolist()
    ##print("x:", x)
    ##print("y:", y)

    plot = plt.figure()
    plt.plot(x, y)
    plt.savefig("dailyplot.jpg")
    print("Figure saved to file")
    ##plt.show()

if __name__ == '__main__':
    ##multithreading for lolz. 
    ##Ultimately going to try separate processes for each battery class, water level monitor
    p = Process(target = readData, args=(0,))
    p.start()
    p.join()