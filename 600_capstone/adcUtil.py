# Don't modify this function.
# If you want to use a different function, include it with your submission.

import spidev

def baseADC(channel=0, device=0):
    bus = 0
    
    spi = spidev.SpiDev()                    # Create a new spidev object
    spi.open(bus,device)                     # Open communication on bus and device (CE0,CE1)
    spi.max_speed_hz = int(1e5)              # Set clock speed to 100 kHz

    if(channel==0): config = [0b01101000, 0] # Measure from channel 0
    else:           config = [0b01111000, 0] # Measure from channel 1

    myBytes = spi.xfer2(config)              # Send and get an array of 2 bytes from ADC
    myData = (myBytes[0] << 8) | myBytes[1]  # Convert returned bytes to integer value

    spi.close()                              # Stop communication with ADC

    return myData                            # Return integer value


def readADC(channel=0, device=0):

    myData = baseADC(channel,device)
    return myData * 3.3 / 1023               # Return voltage from 0V to 3.3V