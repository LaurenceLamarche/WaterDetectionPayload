import serial
import time
import os
import sys

# Replace 'COM_PORT' with your device file '/dev/tty.usbserial-A900LFQY'
uart_id = 0
baud_rate = 115200
print("running start script...")
sys.stdout.flush()

try: 
    ser = serial.Serial('/dev/tty.usbserial-A900LFQY', baud_rate, timeout=1)
except FileNotFoundError:
    print("UART adapter not found at its expected location")
    
# Call the main function

try:
    print("Sending start command to PICO...")
    ser.write(b"MEASURE\n")
    
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            
except KeyboardInterrupt:
    ser.close()
