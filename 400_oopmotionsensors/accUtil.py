# Don't modify this module!
# Write a different module if you want to use different functions,
# and include it with your submission.

import smbus

################################################################################
def readMMA8452Q(i2cport=1):    
    
    # create a new smbus object
    # :: receives the bus index (defaults to 1)
    bus = smbus.SMBus(i2cport)  

    # the device address id 0b0011101 or in hex 0x1D
    AA = 0x1D # Accelerometer Address
        
    # set to active mode to read from registers    
    # :: the control register is in hex 0x2A
    CTRL_REG1 = 0x2A
    bus.write_byte_data(AA,         # set the device address
                        CTRL_REG1,  # set the register
                        0b00000001) # 00 (auto wake) 
                                    # 000 (800Hz data rate) 
                                    # 0 (noise mode) 0 (read mode) 1 (active mode)

    # read data from registers
    # :: registers 0x01 and 0x02 for the x axis (1 byte each)
    # :: registers 0x03 and 0x04 for the y axis (1 byte each)
    # :: registers 0x05 and 0x06 for the z axis (1 byte each)
    data = bus.read_i2c_block_data(AA,   # set the device address
                                   0x01, # set the register
                                   6)    # number of bytes to read

    # convert data from registers to single numbers
    # :: concatenate 8 bits from the first register
    # ::        with 4 bits from the second register
    xRaw = (data[0] << 4) + (data[1] >> 4)
    yRaw = (data[2] << 4) + (data[3] >> 4)
    zRaw = (data[4] << 4) + (data[5] >> 4)

    # fix for 2's complement numbers
    # :: subtract 2^12 if the number is negative
    if xRaw >> 11 == 1: xRaw -= 2**12
    if yRaw >> 11 == 1: yRaw -= 2**12
    if zRaw >> 11 == 1: zRaw -= 2**12
    
    # convert to acceleration in m/s^2
    # :: use the default +/- 2g range (1g per 1024 units)
    toAcc = 9.81 / 1024 
    xAcc = xRaw * toAcc
    yAcc = yRaw * toAcc
    zAcc = zRaw * toAcc

    # return acceleration tuple
    return xAcc,yAcc,zAcc

################################################################################
def readLIS3DH(i2cport=1):
    
    # create a new smbus object
    # :: receives the bus index (defaults to 1)
    bus = smbus.SMBus(i2cport)

    # the device address id 0b0011101 or in hex 0x19
    AA = 0x19 # Accelerometer Address
    
    # use CTRL_REG1 (20h) to enable x,y,z acceleration
    CTRL_REG1 = 0x20    
    bus.write_byte_data(AA,         # set the device address
                        CTRL_REG1,  # set the register
                        0b01110111) # 0111 (400kHz) 
                                    # 0 (normal mode) 
                                    # 111 (enable xyz)
    
    # read data from registers
    OUTX_REG = 0x28
    xLSB = bus.read_i2c_block_data(AA, OUTX_REG,   1)
    xMSB = bus.read_i2c_block_data(AA, OUTX_REG+1, 1)

    OUTY_REG = 0x2A
    yLSB = bus.read_i2c_block_data(AA, OUTY_REG,   1)
    yMSB = bus.read_i2c_block_data(AA, OUTY_REG+1, 1)
    
    OUTZ_REG = 0x2C
    zLSB = bus.read_i2c_block_data(AA, OUTZ_REG,   1)
    zMSB = bus.read_i2c_block_data(AA, OUTZ_REG+1, 1)
    
    # use CTRL_REG1 (20h) to set power down mode
    #bus.write_byte_data(AA, CTRL_REG1, 0b00000000)
    
    # convert data from registers to single numbers
    # :: concatenate 8 bits from the first register
    # ::        with 4 bits from the second register
    xRaw = (xMSB[0] << 4) + (xLSB[0] >> 4)
    yRaw = (yMSB[0] << 4) + (yLSB[0] >> 4)
    zRaw = (zMSB[0] << 4) + (zLSB[0] >> 4)
    
    # fix for 2's complement numbers
    # :: subtract 2^12 if the number is negative
    if xRaw >> 11 == 1: xRaw -= 2**12
    if yRaw >> 11 == 1: yRaw -= 2**12
    if zRaw >> 11 == 1: zRaw -= 2**12
    
    # convert to acceleration in m/s^2
    # :: use the default +/- 2g range (1g per 1024 units)
    toAcc = 9.81 / 1024 
    xAcc = xRaw * toAcc
    yAcc = yRaw * toAcc
    zAcc = zRaw * toAcc
    
    # return acceleration tuple
    return xAcc,yAcc,zAcc

################################################################################
def readACC(model="LIS3DH",i2cport=1):
    if model == "MMA8452Q":
        ax,ay,az = readMMA8452Q(i2cport)
    else:
        ax,ay,az = readLIS3DH  (i2cport)
        
    return ax,ay,az