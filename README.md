# Blue-Iris-POS-Transaction-Overlay
Use the Blue Iris macros feature to display transaction data from Verifone Ruby &amp; TOPAZ POS registers.

#  Prereqs:
python -m pip install pyserial

# Serial Pinout
Only 2 pins need to be connected to the COM port (GND & RX). POS system needs to configured to output DVR data via serial on COM5 in the POS settings. Google verifone topaz backdoor codes to gain access to these configuration options.
