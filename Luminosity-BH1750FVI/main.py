# 
# Minimal luminosity sensor demo using the I2C bus.
# Wiring LoPy - BH1750FVI: GND-GND, 3V3-VCC, P9-SDA, P10-SCL
# Link source: https://docs.pycom.io/pycom_esp32/pycom_esp32/tutorial/includes/i2c.html
# Link LoPy: https://www.pycom.io/wp-content/uploads/2016/11/lopy_pinout.pdf
# 
from machine import I2C
import bh1750fvi
import time

i2c = I2C(0, I2C.MASTER, baudrate=100000)
light_sensor = bh1750fvi.BH1750FVI(i2c, addr=i2c.scan()[0])

while(True):
    data = light_sensor.read()
    print(data)
    time.sleep(1)
