# TESTING WITH THE OLD TEST SETUP (LAURENCE)
# =========================================== #
# This main method is responsible for listening
# TODO: Add more commands here
# =========================================== #

import time
import utime
from machine import Pin, I2C, UART
#import ADSlib
# from easy_comms import Easy_comms
#from ir_rx.print_error import print_error
#from ir_rx.nec import NEC_8
from DataCollection import DataCollection
#from IR_remote import IR_remote

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


# TODO: Verify if we want this here or in the loop
a = DataCollection()
# TODO: JUST TESTING, remove this
#a.start_collection()

measure = False

while True:
    ground_command = read(com1)
    
    if ground_command == "MEASURE":
        print("Receive START command from ground")
        a = DataCollection()
        try:
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
