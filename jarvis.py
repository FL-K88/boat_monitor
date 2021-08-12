#!/usr/bin/python

# ----------------------------------------------------------------------------
#                   BoatMonitor Version 1.0  August 2021
#   This is a Python 3 script for sending data from
#   from a Raspberry Pi 4 and an interface board.
#   It reports on various parameters
#   on a boat under these conditions which are checked every 5min:
#       1. if shore power is off
#       2. if batteries are below 12vdc
#       3. if bilge pump has cycled more than once in a 5min period
#       4. if temperature in the saloon is < 40 degrees or > 85 degrees  ####CHANGE TO ENGINE COMPARTMENT
#   All of the parameters are sent regularly
#   to a web site provided by Inital State where I have a dashboard that  ###CHANGE DELIVERY TO EMAIL DROP
#   shows all of the data in a neat display.
#   The script runs continuously until Ctrl-C is pressed.                  ###CHANGE TO ESCAPE KEY??
#   The SMTP configuration file must be edited and GMail account set up.
#   sudo nano /etc/ssmtp/ssmtp.conf
# ----------------------------------------------------------------------------

import time
import smtplib
import spidev
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor, Unit
import os
import datetime
##from ISStreamer.Streamer import Streamer
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

 # Set your parameters
RepTime = 800  # Time of day that status report will be sent
SleepTime = 5  # number of minutes to sleep in infinte loop between checks
LowVolts = 12  # Battery voltage considered low
LowTemp = 40   # Low temperature in boat
HighTemp = 85  # High temperature in boat
  
global PumpCyclesDay
global SPstate
global Temperature
global Bat1Volts
global Bat2Volts
global Bat3Volts ##New var. Not included in code
global Bat4Volts ##New var. Not included in code
global Bat5Volts ##New var. Not included in code
global Bat6Volts ##New var. Not included in code
DailyReport = 1
CyclePin = 11  # Raspberry pin for monitoring bilge pump cycles -- GPIO 17
ShorePin = 13  # Raspberry pin for monitoring shore power -- GPIO 27
TempPin = 7    # This is the default in W1ThermSensor -- GPIO 4
Bat1Ch = 0     # These are the channels on the ADC MCP3008
Bat2Ch = 1
 

# For getting battery voltags from ADC MCP3008 chip
# Open SPI bus
# spi = spidev.SpiDev()
# spi.open(0,0)

def ReadChannel(channel) :
    # adc = spi.xfer2([1,(8+channel)<<4,0])
    # data = ((adc[1]&3) << 8) + adc[2]
    data = mcp.read_adc(channel)
    return data

def ConvertVolts(data,places) :
    volts = (((data * 3.3) / float(1023)) * 6.20)   # based on having 10k and 2.0k voltage divder
    volts = round(volts, places) # to keep input to GPIO below 3.3v for 12v batteris
    return volts

# def Time(tm_year,tm_mon,tm_mday,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst)

def TOD() :
    data = 100 * time.localtime().tm_hour + time.localtime().tm_min
    return data

def Day() :
    data = time.localtime().tm_yday
    return data

def Date() :
    data = time.asctime()
    return data

StartDay = Day()
TimeStart = TOD()  
#
# GPIO.input(CyclePin)  #  Low = 0 High = 1 on pin
# GPIO.input(ShorePin)
# 
def CountCycles(channel) :  # Call back function to watch bilge pump cycles
    global PumpCyclesDay
    global PumpCyclesPer
    PumpCyclesDay += 1
    PumpCyclesPer += 1
    print("CountCycles called %d" % PumpCyclesPer)

def ShorePowerOff(channel) :
    global SPstate
    SPstate = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(CyclePin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ShorePin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(CyclePin, GPIO.RISING, callback=CountCycles, bouncetime=500)
GPIO.add_event_detect(ShorePin, GPIO.RISING, callback=ShorePowerOff, bouncetime=200)

GPIO.add_event_callback(CyclePin, CountCycles)
GPIO.add_event_callback(ShorePin, ShorePowerOff)

PumpCyclesDay = 0
PumpCyclesPer = 0
SPstate = 1

# Set up temperature features
sensor = W1ThermSensor()


##############################
logList = []
# Set up Steamer functions to log data to my Initial State web site
##BoatLog = Streamer(bucket_name='boat', bucket_key='boat', access_key='ACCESS KEY') ###PUT LOGGING MODULE HERE
logData = {'timestamp': datetime.datetime(), 'tempFarenheit': Temperature, 'bilgeCycles': bilgeCycles, 'shorePowerStatus': shorePowerStatus, 'Bat1Volts': Bat1Volts, 'Bat2Volts': Bat2Volts, 'Bat3Volts': Bat3Volts, 'Bat4Volts': Bat4Volts, 'Bat5Volts': Bat5Volts, 'Bat6Volts':  Bat6Volts}
logList.append(logData)
############################


def Logger() :
    BoatLog.log("Bilge Pump Cycles", PumpCyclesPer)
    BoatLog.log("Shore Power State", SPstate)
    BoatLog.log("Temperature", Temperature)
    BoatLog.log("Starter Battery", Bat1Volts)
    BoatLog.log("House Battery", Bat2Volts)

print("Boat on line.")
print("Start: %s" % Date())

# begin infinite loop until press Ctrl-C to stop
while 1 : 
    SPstate = 1
    if GPIO.input(ShorePin) :
        SPstate = 0
    Temperature = round(sensor.get_temperature(W1ThermSensor.DEGREES_F), 1)
    Bat1Volts = ConvertVolts(ReadChannel(Bat1Ch),2)
    Bat2Volts = ConvertVolts(ReadChannel(Bat2Ch),2)
    Logger()
    if Day() > StartDay :
        DailyReport = 1
        StartDay = Day()
    if StartDay == 1 :  # Check for new year
        DailyReport = 1
    if PumpCyclesPer >= 1 :
        message = "%s \n" % Date
        message = message + "Bilge pump cycles are %d" % PumpCyclesPer
        PumpCyclesPer = 0
        print(message)
    if Temperature < LowTemp :
        message = "%s \n" % Date
        message = message + "Boat temperature is low: %d" % Temperature
        print(message)
    elif Temperature > HighTemp:
        message = "%s \n" % Date
        message = message + "Boat temperature is high: %d" % Temperature
        print(message)
    if SPstate == 0 :
        message = "%s \n" % Date
        message = message + "ShorePower is off"
        print(message)
    if Bat1Volts < 11.5 :
        message = "%s \n" % Date
        message = message + "Starter battery is low: %d" % Bat1Volts
        print(message)
    if Bat2Volts < 11.5 :
        message = "%s \n" % Date
        message = message + "House battery is low: %d" % Bat2Volts
        print(message)
    CurTime = TOD()
    if DailyReport :
        if CurTime >= RepTime :
            DailyReport = 0        
            # put daily report here
            Today = Date()
            message = "Daily Report %s \n" % Today
            message = message + "Temperature: %d \n" % Temperature
            message = message + "Bilge Pump Cycles: %d \n" % PumpCyclesDay
            message = message + "Shore Power: %d \n" % SPstate
            message = message + "Starter Battery: %d \n" % Bat1Volts
            message = message + "House Battery: %d \n" % Bat2Volts
            print(message)
            PumpCyclesDay = 0
    time.sleep(SleepTime * 60)