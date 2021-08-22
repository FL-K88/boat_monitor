import matplotlib.pyplot as plt
import numpy as np
import datetime
import array as arr

##Create 2 methods that receive a list of dictionaries and returns a series of graphs.
##Method 1: Daily Report
##Method 2: Rolling Monthly Report
##Why two separate methods? Is that really necessary?

logList = []

###TEMP: Faked data for the charts. Should be provided by Jarvis.py
for i in range(0,24):
    Bat1Volts = 13.45
    bilgeCycles = i
    Temperature = 87.5
    shorePowerStatus = True
    logData = {'tempFarenheit': Temperature, 'bilgeCycles': bilgeCycles, 'shorePowerStatus': shorePowerStatus, 'Bat1Volts': Bat1Volts}
    logList.append(logData)
###END TEMP

##Set up a line chart item with the past 24 hours of data.
def daily_report(logList, dict_entry):
    x_values = []
    y_values = []
    for i in range (0,24): 
        x_values.append(i) ###Should this be a timestamp from the datastructure instead?
        insert_value = logList[i]
        y_values.append(insert_value[dict_entry])
    plt.plot(x_values,y_values, label = dict_entry)

def monthly_report(logList, dict_entry):
    x_values = []
    y_values = []
    for i in range (0, (24 * 30)): 
        x_values.append(i) ###Should this be a timestamp from the datastructure instead?
        insert_value = logList[i]
        y_values.append(insert_value[dict_entry])
    plt.plot(x_values,y_values, label = dict_entry) ##Figure out how to scale the x-values in a more practical manner


daily_report(logList, 'tempFarenheit')
daily_report(logList, 'bilgeCycles')
daily_report(logList, 'Bat1Volts')
daily_report(logList, 'shorePowerStatus')
plt.legend()
##NOTE IF Y VALUES ARE DIFFERENT, plt.show MAY BREAK. NEED ERROR HANDLING HERE.
plt.show()

##def monthly_report(dataList):
