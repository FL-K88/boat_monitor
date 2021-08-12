import matplotlib.pyplot as plt
import numpy as np
import datetime
import array


##Create 2 methods that receive a list of dictionaries and returns a series of graphs.

##Method 1: Daily Report

##Method 2: Rolling Monthly Report

##Why two separate methods? Is that really necessary?
Bat1Volts = 13.45
bilgeCycles = 2
Temperature = 87.5
shorePowerStatus = True
logList = []
logData = {'tempFarenheit': Temperature, 'bilgeCycles': bilgeCycles, 'shorePowerStatus': shorePowerStatus, 'Bat1Volts': Bat1Volts}
logList.append(logData)

def daily_report(dataList):

    list1 = []
    list2 = []
    list3 = []
    listy1 = []
    listy2 = []
    listy3 = []
    ##line chart showing voltage for each of 6 house batteries

    ##line chart showing bilge pump runs + water level?

    #line chart showing temperature

    ##x = the count of each dict in datalist
    ##y = the values of one variable for all the dictionaries in datalist
    for line in range(len(dataList) - 24, len(dataList)): ##grabs the most recent hourly entries
        list1.append(dataList[line]['Bat1Volts'])#House batteries####NEED TO INCLUDE FOR MULTIPLE BATTERIES ON SAME CHART
        list2.append(dataList[line]['bilgeCycles'])#House batteries####NEED TO INCLUDE FOR MULTIPLE BATTERIES ON SAME CHART
        list3.append(dataList[line]['tempFarenheit'])#House batteries####NEED TO INCLUDE FOR MULTIPLE BATTERIES ON SAME CHART
        listy1.append(line) 
        listy2.append(line) 
        listy3.append(line) 

    x1 = array(list1)
    x2 = array(list2)
    x3 = array(list3)
    y1 = array(listy1)
    y2 = array(listy2)
    y3 = array(listy3)

    fig, (ax1, ax2) = plt.subplots(2, sharey=False)
    ax1.plot(x1, y1, 'ko-')
    ax1.set(title='Daily Summary', ylabel='House Batteries (Volts)')
    ax2.plot(x2, y2, 'r.-')
    ax2.set(xlabel='Time of Day', ylabel='Bilge Pump Runs')
    ##ax3.plot(x3, y3, 'r.-')
    ##ax3.set(xlabel='Time of Day', ylabel='Temperature (F)')
    print("report finished!")
    plt.show()


##def monthly_report(dataList):
