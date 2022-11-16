## to find current ports: portData = serial.tools.list_ports.comports() OR python -m serial.tools.list_ports

###OVERVIEW:###
##sample one data point per hour, per class
##save results to file
##sleep
##@EOD, create report
##@EOW, create summary
##IF file entries > 1 year, delete the oldest entries

import datetime
import csv
import os
from os import getcwd
import time
import serial
from multiprocessing import Process
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import classes ##definitions of the assets being monitored
import random
import sms_alert

########NOTE: NEED TO CONVERT ALL FILEPATHS TO LINUX/PI)#########

####LOGDATA FORMAT: 2022-10-19 01:24:58.752709 voltagefloat ######


CRITICAL_BATTERY_LEVEL = 11.75
def readData(logData, selector):
    ser = [serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 10)] ##[Arduino Leonardo]
    while 1:
        ##arduino transmits 1 voltage reading per second to the pi.
        arduinoData = ser[selector].readline().decode('ascii')
        arduinoData = float(arduinoData.strip("\r\n"))

        if isinstance(arduinoData,float) == False:
            print("voltage stored as " + str(type(arduinoData)) + ", not float")
        
        ##Store data by timestamp
        data = [datetime.datetime.now(), arduinoData]

        ##drop the earliest element if more than a year's worth of data is stored ##NOTE: Change to edit at the document level
        if len(logData) > (24*366):
            del logData[0]

        logData.append(data)
        print(logData[-1]) ## print datapoint just added
        if data[1] < CRITICAL_BATTERY_LEVEL:
            sendAlert(data)
        if len(logData) > 23:
            dailyPlot(logData)
            exit()
        time.sleep(1) ##In seconds. Eventually change to 3600/1 hour

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
    plt.savefig("dailyplot_" + str(time.time()) + ".jpg")
    print("Figure saved to file")
    ##plt.show()

def weeklyPlot(logData):
    sl = slice(-168,-1) 
    data = logData[sl]
    data.append(logData[-1]) ##accounts for slice not including final element
    maxDate = data[0][0] ##assumes logData is ordered with first element earliest
    minDate = data[-1][0]

    ## print(minDate.strftime('%Y-%m-%d'))
    ## print(maxDate.strftime('%Y-%m-%d'))
    x = np.arange(start=0,stop=168,step=1) ## time offset. Temporary. Insures chart is getting only ints and floats
    y = np.asarray(data)[:,1]
    if not isinstance(x, list):
        x = x.tolist()
    if not isinstance(y, list):
        y = y.tolist()
    ##print("x:", x)
    ##print("y:", y)

    plot = plt.figure()
    plt.plot(x, y)
    plt.savefig("dailyplot_" + str(time.time()) + ".jpg")
    print("Figure saved to file")
    ##plt.show()


##NOT FINISHED
def sendAlert(data):
    print("Alert Here using sms_alert")

def storeData(logData): ##Not tested. Try alternate method if log is overwriting data in the csv or this method creates too many files
    if(isinstance(logData, list)):
        ##filename = getcwd() + "/data/" + str(time.localtime(time.time())) + ".csv"
        csvOut = open(getcwd() + '\\data\\log.csv', mode='a', newline='')
        writer = csv.writer(csvOut, delimiter=',')
        writer.writerows(logData)
        csvOut.close()
        print("Data logged to ",  csvOut)
    else:
        print("Error: logData input must be a pandas dataframe.")

def readData():
    with open(getcwd() + '\\data\\log.csv', newline='') as read_file:
        csv_reader = csv.reader(read_file)
        data = list(csv_reader)
        print(data)
        return data

##allows testing without actively accessing the arduino. Takes place of ReadData
def simulateData(logData, number_of_entries):
    for i in range(0,number_of_entries - 1):
        data = [datetime.datetime.now(), round(random.uniform(15.50, 8.25),2)]
        logData.append(data)
        print(logData[-1]) ## print datapoint just added
        if len(logData) > number_of_entries - 1:
            ##dailyPlot(logData)
            exit()
        ##time.sleep(1) ##In seconds. Eventually change to 3600/1 hour
    return logData

def testRun():
    logData = []
    logData = simulateData(logData, 168)
    storeData(logData)
    data = readData()
    ##monthly/weekly plotting logic here
    ##dailyPlot(data)
    ##weeklyPlot(data)
    ##monthlyPlot(data)

def execute(selector): ##live run
    logData = []
    readData(logData, selector)

if __name__ == '__main__':
    ##multithreading for lolz. 
    ##Ultimately going to try separate processes for each battery class (3), water level monitor (1)
    ##p = Process(target = execute, args=(0,))
    ##p = Process(target = testRun)
    ##p.start()
    ##p.join()
    testRun()





