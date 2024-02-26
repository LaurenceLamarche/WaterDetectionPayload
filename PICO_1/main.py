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

# Define the PWM pins for the LEDs
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
a = DataCollection()
# TODO: JUST TESTING, remove this
#a.start_collection()


measure = False
#num_samples = 1
while True:
    ground_command = read(com1)
    #print(ground_command)
    if ground_command == "MEASURE":
        print("Received START command from ground")
        #a = DataCollection()
        try:
            write(com1, "STARTED")
            # Attempt to start data collection
            #a.start_collection()
            led_number, step_count = a.start_collection()
        except KeyboardInterrupt:
            # If KeyboardInterrupt occurs (e.g., Ctrl+C is pressed)
            # Handle the interruption here
            print(f"Data collection interrupted at LED number {led_number} and step count {step_count}")
            # Perform actions based on the interruption
        finally:
            measure = False




