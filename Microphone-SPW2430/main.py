#
# Minimal MEMS microphone demo using the onboard analog digital converter (ADC)
# Wiring LoPy - SPW2430: GND-GND, 3V3-VIN, P16-DC
# Link ADC: https://docs.pycom.io/pycom_esp32/library/machine.ADC.html
# Link SPW2430: https://www.adafruit.com/product/2716
# Link LoPy: https://www.pycom.io/wp-content/uploads/2016/11/lopy_pinout.pdf
#
from machine import Pin
from network import LoRa

import machine
import pycom
import time
import socket
import binascii
import struct

# switch off the default LoPy LED heartbeat
pycom.heartbeat(False)
pycom.rgbled(0)

noise_output = ".**********************************************************************"
noise_samples = 2000
noise_damping = 30
toggleled = True

starttime = time.time()

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

# Create a socket to communicate with TheThingsNetwork
def create_ttn_socket():
    join_ttn()

    ttn_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    ttn_sock.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    ttn_sock.setblocking(False)

    return ttn_sock

# Join TheThingsNetwork
def join_ttn():
    # Initialize LoRa in LORAWAN mode.
    lora = LoRa(mode=LoRa.LORAWAN, sf=7, tx_power=14)
    lora.BW_125KHZ
    lora.CODING_4_5

    # Create an ABP authentication params using parameter from TheThingsNetwork:
    # https://console.thethingsnetwork.org/applications/<your-app>/devices/<your-device>
    device_address = '26011166'
    network_session_key = 'F1D8844A98DD537D5DBEFD27CDA79E5A'
    app_session_key = 'C4D5827A715F802850355439EFB31880'

    # Join TTN using ABP (Activation By Personalization)
    da = struct.unpack(">l", binascii.unhexlify(device_address.replace(' ','')))[0]
    nsk = binascii.unhexlify(network_session_key.replace(' ',''))
    ask = binascii.unhexlify(app_session_key.replace(' ',''))
    lora.join(activation=LoRa.ABP, auth=(da, nsk, ask))

    # Wait for join OK
    while not lora.has_joined():
        print('Joining The Things Network ...' )
        time.sleep(1)

    print('Sussessfully joined The Things Network')

# Create the button object (representing the LoPy user button)
def create_button():
    button = Pin("G17", Pin.IN, pull=Pin.PULL_UP)
    button.callback(Pin.IRQ_RISING, button_handler) # Interrupt on raising signal

    return button

# Interrupt handler for button
def button_handler(arg):
    button.callback(Pin.IRQ_RISING, None) # Deactivate interrupt
    active = 0
    for i in range(20):
        active += button()
        time.sleep_ms(10)

    if active > 15:
        button_action()

    button.callback(Pin.IRQ_RISING, button_handler) # reactivate interrupt

# Pressing the button will send the current counter value to TheThingsNetwork
# Received uplink data is used to set the color LED accordingly
def button_action():
    global sock
    global counter

    data_down = str(counter)
    print('Sending data:',  data_down)
    sock.send(data_down)

    data_up = sock.recv(4)
    print('Recieved data:',  data_up,  'len(data):',  len(data_up))

    if(len(data_up) == 3):
        color = (data_up[0]<<16)|(data_up[1]<<8)|data_up[2]
        print('Update LED')
        pycom.rgbled(color)
    else:
        print('Swich LED off')
        pycom.rgbled(0)

    counter += 1

def send_noise_value(noise):
    global sock

    data_down = str(noise)
    print('Sending noise data:',  data_down)
    sock.send(data_down)

    data_up = sock.recv(4)
    print('Recieved data:',  data_up,  'len(data):',  len(data_up))


# Create LoRa socket and button
sock = create_ttn_socket()
button = create_button()
counter = 0;

# n = Anzahl bisheriger Werte
# avg = Durchschnitt
n = 0
avg = 0

while True:
    noise = getNoise()
    printNoise(noise)
    # print(time.time())

    # n = Anzahl bisheriger Werte
    # avg = Durchschnitt
    # noise = Messwert

    # forever:
    #     avg = (n * avg + noise) / ++n

    avg = (n * avg + noise) / (n+1)
    n = n + 1

    print(avg)

    if (time.time() > starttime+60):
        starttime = time.time()
        send_noise_value(avg)
        avg = 0
        n = 0

        if (toggleled):
            pycom.rgbled(0x00ff00)
            toggleled = False
        else:
            pycom.rgbled(0xff0000)
            toggleled = True

    # print('0x{0:06x}'.format(noise*256*64))
    # pycom.rgbled(noise*256*64)
