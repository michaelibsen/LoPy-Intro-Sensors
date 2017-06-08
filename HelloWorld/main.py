# 
# A slightly extended LoPy "hello world" 
# After startup the LoPy automatically executes the cone in file main.py  (this file)
# 

import pycom
import time

COLORS = [0x220000, 0x111100, 0x002000, 0x000022, 0x110011]
DELAY_MS = 1000

# switch off the default LoPy LED heartbeat
pycom.heartbeat(False)
pycom.rgbled(0)

# the "hello world"
print('hello world''')

while True:
    # cycle through all colors
    for color in COLORS:
        print("color: ",  "0x%0.6X" % color)
        pycom.rgbled(color)
        time.sleep_ms(DELAY_MS)
