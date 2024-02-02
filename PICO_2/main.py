# PICO 2 - (Previously had the Photodetector and sensors)

import time
import utime
from machine import Pin, I2C, UART
# from easy_comms import Easy_comms
from ir_rx.print_error import print_error
from ir_rx.nec import NEC_8

# UART pico communication
uart_id = 0
baud_rate = 115200
com1 = UART(uart_id, baud_rate)
#com1 = Easy_comms(uart_id=0, baud_rate=9600)


def write(com1, message:str):
    print(f'sending message: {message}')
    message = message + '\n'
    com1.write(bytes(message,'utf-8'))
   
#def start(self):
 #   message = "ahoy\n"
  #  print(message)
   # self.send(message)

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

#ir remote pin and values
pin_ir = Pin(13, Pin.IN)
Stop = 28
Start = 24
measure = False

#ADS1115 I2C connection
ADS = I2C(1, freq=400000, scl=Pin(15), sda=Pin(14))
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

def decodeKeyValue(data):
    return data

# User callback for ir remote
def callback(data, addr, ctrl):
    global measure
    if data < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        print(data)
        if data == Start:
            measure = True
        elif data == Stop:
            measure = False
ir = NEC_8(pin_ir, callback)  # Instantiate receiver
ir.error_function(print_error)  # Show debug information

# Main loop

#write(com1, f'off')
motor_is_off = True
count = 0
with open('motorTest1550nm.txt', 'w') as file:
    while True:
        #message = read(com1)
        message = "photodetector"
        if message == "photodetector":
            value = readValue(0)
            value_volts = value*(4.096*2)/(0xffff)
            print("\n",value_volts,"\tVolts\n")
            
            #write(com1, str(value_volts))
            time.sleep(0.006)
            count +=1
            file.write(str(count)+','+ str(value_volts)+ ',\n')
    '''
    if measure == True:
        value = readValue()
        print("\n",(4.096*2)/(0xffff)*(value),"\tVolts\n")
        time.sleep(0.1)
        write(com1, f'on')
        time.sleep(0.05)
    else:
        if not motor_is_off:
            write(com1, f'off')
            motor_is_off = False
        time.sleep(0.05)
    

'''
