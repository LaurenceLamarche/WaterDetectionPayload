# motor pico
# =========================================== #
# This main method is responsible for listening
# TODO: Add more commands here
# =========================================== #

import time
import utime
from machine import Pin, I2C, UART, PWM
#from DataCollection import DataCollection
from DataCollection import DataCollection


# UART pico communication
uart_id = 0
baud_rate = 115200
com1 = UART(uart_id, baud_rate)
#com1 = Easy_comms(uart_id=0, baud_rate=9600)

pwm_max = 2**16 - 1
# Define the PWM pins for the LEDs
# 1200
LED1200_pin = Pin(11)
pwm_LED1200 = PWM(LED1200_pin, freq=400) # Initialize PWM with a frequency of 1000Hz
pwm_LED1200.duty_u16(pwm_max) 
# 1050
LED1050_pin = Pin(12)  # Replace 4 with the GPIO pin number you want to use
pwm_LED1 = PWM(LED1050_pin, freq=400)
pwm_LED1.duty_u16(0)
# 1550
LED1550_pin = Pin(13)  # Replace 4 with the GPIO pin number you want to use
pwm_LED1550 = PWM(LED1550_pin, freq=400)
pwm_LED1550.duty_u16(pwm_max)
# TEC
TEC_pin = Pin(14)  
pwm_TEC = PWM(TEC_pin, freq=400)
pwm_TEC.duty_u16(0)

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

# TODO: Verify if we want this here or in the loop
a = DataCollection(com1)
# TODO: JUST TESTING, remove this
a.start_collection()


measure = False
#num_samples = 1
try:
    while True:
        ground_command = read(com1)
        #print(ground_command)
        if ground_command == "MEASURE":
            print("Received START command from ground")
            #a = DataCollection()
            try:
                write(com1, "STARTED")
                # Attempt to start data collection
                #a = DataCollection()
                led_number, step_count = a.start_collection() # save for when starting again
                print(f"Data collection finished at LED number {led_number} and step count {step_count}")
            except KeyboardInterrupt:
                # If KeyboardInterrupt occurs (e.g., Ctrl+C is pressed)
                # Handle the interruption here
                print(f"Data collection interrupted at LED number {led_number} and step count {step_count}")
                # Perform actions based on the interruption
                com1.deinit() #close the com port
            finally:
                measure = False
                #com1.deinit() #close the com port
        elif ground_command == "SLEEP":
            print("Received SLEEP command from ground")
            try:
                write(com1, "SLEEP MODE ACTIVATED - GOOD NIGHT")
            except KeyboardInterrupt:
                # If KeyboardInterrupt occurs (e.g., Ctrl+C is pressed)
                # Handle the interruption here
                print("Sleep command execution was interrupted")
                # Perform actions based on the interruption
                com1.deinit() #close the com port
            except:
                print("Error sending sleep confirmation")
        
        elif ground_command == "STOP":
            print("Received SLEEP command from ground, but Data Collection not running")
        
        elif ground_command == "REVERSE":
            print("Received REVERSE command from ground, direction will be changed for the next data collection loop")
            try:
                a.change_direction()
                write(com1, "Motor direction changed for next time")
            except KeyboardInterrupt:
                # If KeyboardInterrupt occurs (e.g., Ctrl+C is pressed)
                # Handle the interruption here
                print("Reverse command execution was interrupted")
                # Perform actions based on the interruption
                com1.deinit() #close the com port
            except:
                print("Error sending motor reversing confirmation")
except KeyboardInterrupt:
    if (com1):
        com1.deinit() #close the com port when interrupted



