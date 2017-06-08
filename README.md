# LoPy Hello World and Sensors Introduction

**Please Note**: Work in progress

## Summary

This repo contains sample code on how to start with LoPy prgramming and use some sensors with the LoPy microcontroller.

1. Hello World (slightly extended)
2. MEMS microphone
3. Ambient light sensor
4. Temperature sensor

The sections below provide further information for each sensor covered

## Hello World

The folder HelloWorld contains a sightly extended LoPy "Hello World" example. 
In addition to printing "Hello World" the demo also cycles through some colors using the LoPy onboard RGB LED.

## MEMS microphone

The folder Microphone-SPW2430 contains a minimal MEMS microphone demo to measure noise levels using the LoPy onboard 
analog digital converter (ADC). 

### Links
* [TTN noise measuring use case (blog post)](https://dzone.com/articles/the-things-network-and-eclipse-scout)
* [LoPy ADC information (official docs)](https://docs.pycom.io/pycom_esp32/library/machine.ADC.html)
* [SPW2430 microphone (Adafruit breakout board)](https://www.adafruit.com/product/2716)
* [LoPy pinout](https://www.pycom.io/wp-content/uploads/2016/11/lopy_pinout.pdf)

## Ambient light sensor

The folder Luminosity-BH1750FVI contains the sample code for the BH1750FVI luminosity sensor.
The LoPy microprocessor taks over the I2C bus with this sensor.

The demo cosists of the following files
* main.py: Prints the current luminosity every second on the console
* bh1750fvi.py: Class for the I2Configuration for the BH1750FVI

### I2C

The I2C bus has just two wires called SCL and SDA. 
SCL is the clock line. It is used to synchronize all data transfers over the I2C bus. 
SDA is the data line. The SCL & SDA lines are connected to all devices on the I2C bus. 
There needs to be a third wire which is just the ground or 0 volts. 
There may also be a power wire to feed the devices. In our case, 3.3V will do.

### Hardware Wiring

On the BH1750FVI sensor side we use the following pins:

* SCL
* SDA 
* GND
* VCC (3.3V power)

The wiring with the LoPy is as follows (LoPy to BH1750FVI)

* P9 to SDA
* P10 to SCL
* GND to GND
* 3V3 to VCC

### Links
* [Using the I2C Bus](http://www.robot-electronics.co.uk/i2c-tutorial)
* [Source of example code](https://docs.pycom.io/pycom_esp32/pycom_esp32/tutorial/includes/i2c.html)
* [Ambient light sensor BH1750FVI breakout board](http://www.play-zone.ch/en/digitaler-ambient-light-sensor-mit-bh1750fvi.html?___from_store=de)
* [LoPy pinout](https://www.pycom.io/wp-content/uploads/2016/11/lopy_pinout.pdf)

## Temperature sensor

TODO
