# motor pico
# =========================================== #
# This main method is responsible for listening
# for IR remote commands:
# 2 = Start Data Collection (move the motor)
# TODO: Add more commands here
# =========================================== #

import time
import utime
from machine import Pin, I2C, UART
from DataCollection import DataCollection

# UART pico communication
uart_id = 0
baud_rate = 115200
com1 = UART(uart_id, baud_rate)

def write(com1, message:str):
    print(f'sending message: {message}')
    message = message + '\n'
    com1.write(bytes(message,'utf-8'))

def read(com1):
    timeout = 1000000000 # 1 second
    start_time = time.time_ns()
    current_time = start_time
    message_end = False
    message = ""
    while (not message_end) and (current_time <= (start_time + timeout)):
        current_time = time.time_ns()
        if (com1.any() > 0):
            #print(com1.read())
            message = message + com1.read().decode('utf-8')
            if '\n' in message:
                message_end = True
                message = message.strip('\n')
                # print(f'received message: {message}')
                return message
    else:
        return None


#ADS1115 I2C connection
#ADS = I2C(1, freq=400000, scl=Pin(15), sda=Pin(14)) # PICO 2 I2C PINS

ADS = I2C(1, freq=400000, scl=Pin(11), sda=Pin(10)) # PICO 1 12C PINS
address = 72
def readConfig():
    ADS.writeto(address, bytearray([1]))
    result = ADS.readfrom(address, 2)
    return result[0]<<8 | result[1]

def readValue(channel):
    ADS.writeto(address, bytearray([0]))
    result = ADS.readfrom(address, 2)
    
    config = readConfig()
    config &= ~(7<<12) & ~(7<<9)
    config |= (7 & (4+channel))<<12
    config |= (1<<9) #gain of 4.096 V
    config |= (1<<15)
    
    config = [ int(config>>i & 0xff) for i in (8,0)]
    ADS.writeto(address, bytearray([1] + config))
    
    config = readConfig()
    while (config & 0x8000) ==0:
        config = readConfig()
    
    ADS.writeto(address, bytearray([0]))
    result = ADS.readfrom(address, 2)
    return result[0]<<8 | result[0]

# FOR TESTING
a = DataCollection()
a.start_collection()


