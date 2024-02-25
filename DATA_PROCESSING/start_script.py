import serial
import time
import os
import sys

# Replace 'COM_PORT' with your device file '/dev/tty.usbserial-A900LFQY'
uart_id = 0
baud_rate = 115200
print("running start script...")
sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG

try: 
    ser = serial.Serial('/dev/tty.usbserial-A900LFQY', baud_rate, timeout=1)
except FileNotFoundError:
    print("UART adapter not found at its expected location")
    sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG
    
# Call the main function

try:
    print("Sending start command to PICO...")
    sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG
    ser.write(b"MEASURE\n")
    
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            print(data)
            sys.stdout.flush()
            if data == "MEASURE_RECEIVED":
                sys.exit()
            
except KeyboardInterrupt:
    ser.close()
