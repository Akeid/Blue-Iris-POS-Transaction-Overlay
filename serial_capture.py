import serial
import time
import datetime
import os


from time import sleep
from collections import deque

# ***********CONFIG*************
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

#Register Name for record keeping purposes (Change this to whatever you want)
registerNUM = "102"

#Serial Port/RS232 com port
PORT_COM = "COM5"

#Name of the clipboard file that will hold the current transaction data
clipboardFile = "log_102.txt"

#The maximum amount of transaction lines to display on screen
maxOverlayLines = 9

#The time to keep the last transaction on screen after it has been completed (seconds)
wipeTime = 4.5
# *******************************

#establish serial instance
ser = serial.Serial(
    port=PORT_COM,\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("Connected to: " + ser.portstr)

#Wrties the transaction to a folder with the date as the file name for all the transactions captured
def writeToDailyLog(lineData):
    with open(THIS_FOLDER + "\\" + registerNUM + "\\" + str(datetime.date.today()) + ".txt", "a+") as f:
        f.write(lineData)

#Writes current transaction to the clipboard log file
def writeToTransClipboard(clipboardData):
    try:
        with open(clipboardFile, 'r') as file:
            lines = deque(file, maxOverlayLines)
            lines.append(clipboardData)
        with open(clipboardFile, 'w') as file:
            file.writelines(lines)
            print(clipboardData)

    except PermissionError:
        print("Permission error occured in the writeToTransClipboard() function, trying again...")
        sleep(1)

#Wipe the clipboard file, called when the current transaction is cashed out and a new transaction begins
def wipeTransClipboard():
    open(clipboardFile, 'w').close()
    #print("Transaction Clipboard Wipped...")

#Store incoming serial data
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
                writeToDailyLog("***********************************************\n")                               
                writeToDailyLog(formated_text)               
                sleep(wipeTime)
                wipeTransClipboard()
            else:
                print(formated_text)
                writeToTransClipboard(formated_text)
                writeToDailyLog(formated_text)              
            seq = []
            count += 1
            break

ser.close()
