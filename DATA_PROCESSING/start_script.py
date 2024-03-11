# import serial
# import time
# import os
# import sys
# import signal

# # Example cleanup function
# def clean_exit(signum, frame):
#     print("Closing the sleep script...")
#     sys.stdout.flush()
#     # Close the serial connection
#     ser.close()
#     sys.exit(0)

# # Register the signal handler for clean exit
# signal.signal(signal.SIGINT, clean_exit)

# # Replace 'COM_PORT' with your device file '/dev/tty.usbserial-A900LFQY'
# uart_id = 0
# baud_rate = 115200
# device = '/dev/tty.usbserial-A900LFQY'  # Your device file
# print("Running start script...")
# sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG

# try:
#     ser = serial.Serial(device, baud_rate, timeout=1)
#     ser.write(b"SLEEP\n")
#     ser.flush()
#     print("Sleep command sent.")
#     sys.stdout.flush()
# except FileNotFoundError:
#     print("UART adapter not found at its expected location")
#     sys.stdout.flush()
# except Exception as e:
#     print(f"Error sending sleep command: {str(e)}")
#     sys.stdout.flush()
# finally:
#     if ser:
#         # Close the serial port
#         ser.close()
    

import serial
import sys
import signal

# Setup signal handler for clean exit
def clean_exit(signum, frame):
    print("Cleaning up resources...")
    sys.stdout.flush()
    if 'ser' in globals():
        ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, clean_exit)

# Replace 'COM_PORT' with your device file
uart_id = 0
baud_rate = 115200
device = '/dev/tty.usbserial-A900LFQY'  # Replace with your device file

# Check for command line arguments
if len(sys.argv) != 2 or sys.argv[1] not in ['stop', 'reverse', 'sleep']:
    print("Invalid argument. Use 'stop', 'reverse', or 'sleep'.")
    sys.exit(1)

command = sys.argv[1].upper()

try:
    # Open serial connection
    ser = serial.Serial(device, baud_rate, timeout=1)
    if command == 'SLEEP':
        ser.write(b"SLEEP\n")
    elif command == 'STOP':
        ser.write(b"STOP\n")
    elif command == 'REVERSE':
        ser.write(b"REVERSE\n")
    ser.flush()
    print(f"{command} command sent.")
except FileNotFoundError:
    print("UART adapter not found at its expected location")
except Exception as e:
    print(f"Error sending {command} command: {str(e)}")
finally:
    if 'ser' in globals() and ser.is_open:
        ser.close()

sys.stdout.flush()

