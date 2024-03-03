# motor pico
# =========================================== #
# This main method is responsible for listening
# for IR remote commands:
# 2 = Start Data Collection (move the motor)
# TODO: Add more commands here
# =========================================== #

#import time
#import utime
#from machine import Pin, I2C, UART
#from ir_rx.print_error import print_error
#from ir_rx.nec import NEC_8
from DataCollection import DataCollection
import _thread


# Define the PWM pins for the LEDs and initialize to zero so theres no floating pins
# 1200
LED1200_pin = Pin(11)
pwm_LED1200 = PWM(LED1200_pin, freq=400) # Initialize PWM with a frequency of 1000Hz
pwm_LED1200.duty_u16(0) 
# 1050
LED1050_pin = Pin(12)  # Replace 4 with the GPIO pin number you want to use
pwm_LED1 = PWM(LED1050_pin, freq=400)
pwm_LED1.duty_u16(0)
# 1550
LED1550_pin = Pin(13)  # Replace 4 with the GPIO pin number you want to use
pwm_LED1550 = PWM(LED1550_pin, freq=400)
pwm_LED1550.duty_u16(0)
# TEC
TEC_pin = Pin(14)  
pwm_TEC = PWM(TEC_pin, freq=400)
pwm_TEC.duty_u16(0)

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



'''
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


#ir remote pin and values
pin_ir = Pin(14, Pin.IN)
Stop = 28
Start = 24
change_dir = 82
measure = False

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
            com1.write('photodetector')
            
        elif data == Stop:
            DataCollection.stop = True
            
        elif data == change_dir:
            DataCollection.direction = not DataCollection.direction
ir = NEC_8(pin_ir, callback)  # Instantiate receiver
ir.error_function(print_error)  # Show debug information
'''
a = DataCollection()
# Main loop
measure = True
while True:
    ground_command = read(com1)
    
    if ground_command == "MEASURE":
        print("Received START command from ground")
        
        try:
            write(com1, "STARTED")
            # Attempt to start data collection
            #a.start_collection()
            led_number, step_count = a.start_collection()
        except KeyboardInterrupt:
            # If KeyboardInterrupt occurs (e.g., Ctrl+C is pressed)
            # Handle the interruption here
            #led_number, step_count = a.start_collection()  # Get information about the state
            print(f"Data collection interrupted at LED number {led_number} and step count {step_count}")
            # Perform actions based on the interruption
        finally:
            measure = False
            '''
    if measure == True:
        a = DataCollection()
        second_thread = _thread.start_new_thread(a.temp_control, ())
        a.start_collection()
        measure = False
'''





