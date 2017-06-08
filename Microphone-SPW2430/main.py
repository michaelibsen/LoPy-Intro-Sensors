# 
# Minimal MEMS microphone demo using the onboard analog digital converter (ADC)
# Wiring LoPy - SPW2430: GND-GND, 3V3-VIN, P16-DC
# Link ADC: https://docs.pycom.io/pycom_esp32/library/machine.ADC.html
# Link SPW2430: https://www.adafruit.com/product/2716
# Link LoPy: https://www.pycom.io/wp-content/uploads/2016/11/lopy_pinout.pdf
# 

import machine

noise_output = ".**********************************************************************"
noise_samples = 2000
noise_damping = 30

adc = machine.ADC()             # create an ADC object
noise_pin = adc.channel(pin='P16')   # create an analog pin on P16

def getNoise():
    global noise_samples
    
    vmin = 10000
    vmax = 0
    
    for i in range(0,  noise_samples):
        val = noise_pin()                # read an analog value
        vmax = max(vmax,  val)
        vmin = min(vmin,  val)
            
    return vmax - vmin

def printNoise(noise):
    global noise_output
    global noise_damping
    
    level = int(noise / noise_damping)
    print(noise_output[:level])
    
while True:
    noise = getNoise()
    printNoise(noise)
