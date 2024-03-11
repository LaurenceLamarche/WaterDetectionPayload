import serial
import time
import os
import sys

# Example cleanup function
def clean_exit(signum, frame):
    print("Closing the sleep script...")
    sys.stdout.flush()
    # Close the serial connection
    ser.close()
    sys.exit(0)

# Register the signal handler for clean exit
signal.signal(signal.SIGINT, clean_exit)

# Replace 'COM_PORT' with your device file '/dev/tty.usbserial-A900LFQY'
uart_id = 0
baud_rate = 115200
device = '/dev/tty.usbserial-A900LFQY'  # Your device file
print("Running start script...")
sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG

try:
    ser = serial.Serial(device, baud_rate, timeout=1)
    ser.write(b"SLEEP\n")
    ser.flush()
    print("Sleep command sent.")
    sys.stdout.flush()
except FileNotFoundError:
    print("UART adapter not found at its expected location")
    sys.stdout.flush()
except Exception as e:
    print(f"Error sending sleep command: {str(e)}")
    sys.stdout.flush()
finally:
    if ser:
        # Close the serial port
        ser.close()
    
