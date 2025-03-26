#  *****************************************************************
#  *                                                               *
#  *  Verifone Topaz/Sapphire/Commander Transaction Overlay Logger *
#  * 
#  * ********** By Akeid 2018 ***********
#  *  https://github.com/Akeid/TOPAZ-POS-Overlay                    *
#  *                                                               *
#  *****************************************************************


import serial
import time
import datetime
import os


from time import sleep
from collections import deque


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
registerNUM = "101"
PORT_COM = "COM3"
clipboardFile = "log_101.txt"
maxOverlayLines = 9
wipeTime = 4.5

currentDT = datetime.datetime.now()
timestamp = "[TIME] " + currentDT.strftime("%Y-%m-%d %H:%M:%S") + "\n"


ser = serial.Serial(
    port=PORT_COM,\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=5)

print("connected to: " + ser.portstr)

def writeToDailyLog(lineData):
    #print ("Transation Line detected")
    #print("in pos trans line " + formated_text)
    with open(THIS_FOLDER + "\\" + registerNUM + "\\" + str(datetime.date.today()) + ".txt", "a+") as f:
        f.write(lineData)

def writeToTransClipboard(clipboardData):
    try:
#        with open(clipboardFile, "a+") as f:
#            f.write(clipboardData)
#            print(clipboardData)
        with open(clipboardFile, 'r') as file:
            lines = deque(file, maxOverlayLines)
            lines.append(clipboardData)
        with open(clipboardFile, 'w') as file:
            file.writelines(lines)
            print(clipboardData)

    except PermissionError:
        print("Permission error occured in the writeToTransClipboard() function, trying again...")
        sleep(1)

def wipeTransClipboard():
    open(clipboardFile, 'w').close()
    #print("Transaction Clipboard Wipped...")

#this will store the line
seq = []
count = 1

while True:
    for c in ser.read():
        seq.append(chr(c)) #convert from ANSII
        joined_seq = ''.join(str(v) for v in seq) #Make a string from array
        if chr(c) == '\n':
            text_line = "Line " + str(count) + ': ' + joined_seq
            formated_text = text_line[text_line.find(registerNUM)+4:]
            if "TRAN#" in formated_text:
                writeToDailyLog(timestamp)
                writeToDailyLog("***********************************************\n")
                writeToDailyLog(formated_text)        
                sleep(wipeTime)
                wipeTransClipboard()
            elif "Syncing NAXML Deals" in formated_text:
                wipeTransClipboard()
            else:
                print(formated_text)
                writeToTransClipboard(formated_text)
                writeToDailyLog(formated_text)                
            seq = []
            count += 1
            break

ser.close()
