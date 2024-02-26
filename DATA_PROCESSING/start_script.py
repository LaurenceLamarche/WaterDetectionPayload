import serial
import time
import os
import sys

# Replace 'COM_PORT' with your device file '/dev/tty.usbserial-A900LFQY'
uart_id = 0
baud_rate = 115200
print("Running start script...")
sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG

try: 
    ser = serial.Serial('/dev/tty.usbserial-A900LFQY', baud_rate, timeout=1)
except FileNotFoundError:
    print("UART adapter not found at its expected location")
    sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG
    
# Call the main function
    
# retries = 3
# for _ in range(retries):
#     try:
#         print("Sending start command to PICO...")
#         sys.stdout.flush()
#         ser.write(b"MEASURE\n")
#         ser.flush()
#         time.sleep(0.1)
#         line = ser.readline().decode('utf-8').rstrip()
#         print(line)
#         sys.stdout.flush()
#         if line == "STARTED":
#             print("STARTED")
#             sys.stdout.flush()
#             break  # Exit the loop if the command is sent successfully
#     except KeyboardInterrupt:
#         ser.close()
#     time.sleep(0.1)

started = False
while not started: 
    try:
        print("Sending start command to PICO...")
        sys.stdout.flush()
        ser.write(b"MEASURE\n")
        #ser.flush()
        time.sleep(0.1)
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line == "STARTED":
                print("STARTED")
                sys.stdout.flush()
                started = True  # Exit the loop if the command is sent successfully
    except KeyboardInterrupt:
        ser.close()
    time.sleep(0.1)    

# Close the serial port
ser.close()
    
