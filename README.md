# Blue-Iris-POS-Transaction-Overlay
Use the Blue Iris macros feature to display transaction data from Verifone Ruby &amp; TOPAZ POS registers.

#  Prereqs:
python -m pip install pyserial
  Run python serial_capture.py

# Serial Pinout
Only 2 pins need to be connected to the COM port (GND & RX). POS system needs to configured to output DVR data via serial on COM5 in the POS settings. Google verifone topaz backdoor codes to gain access to these configuration options.

![alt text](https://i.imgur.com/ykmt4Uu.png)

# Connection Scheme
![alt text](https://i.imgur.com/P60xCx9.png)



# Blue Iris
Configure a macro to display the contents of the clipboard log file generated by the script. Go to your desired camera video options and choose overlay and enter the macro ID (ex. %1) to enable the macro.

![alt text](https://i.imgur.com/1kxxJyV.png)

![alt text](https://i.imgur.com/TTH6MPv.png)
