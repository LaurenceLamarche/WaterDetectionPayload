# import serial
# import signal
# import time
# import os
# from datetime import datetime
# import sys

# # Example cleanup function
# def clean_exit(signum, frame):
#     print("Closing the receive script...")
#     sys.stdout.flush()
#     # Close your serial connection here
#     ser.close()
#     sys.exit(0)

# # Register the signal handler for clean exit
# signal.signal(signal.SIGINT, clean_exit)

# # Specify the directory where the files should be saved
# data_directory = os.path.join(os.path.dirname(__file__), 'data')  # Create the data directory inside the current directory
# error_directory = os.path.join(os.path.dirname(__file__), 'error')  # Create the error directory inside the current directory

# # Create the directories if they don't exist
# os.makedirs(data_directory, exist_ok=True)
# os.makedirs(error_directory, exist_ok=True)

# # Replace 'COM_PORT' with your device file '/dev/tty.usbserial-A900LFQY'
# uart_id = 0
# baud_rate = 115200
# print("Running data reception script...")
# sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG
# try:
#     ser = serial.Serial('/dev/tty.usbserial-A900LFQY', baud_rate, timeout=1)
# except FileNotFoundError:
#     print("UART adapter not found at its expected location")
#     sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG


# # Call the main function
# started = False
# while not started:
#     try:
#         print("Sending start command to PICO...")
#         sys.stdout.flush()
#         ser.write(b"MEASURE\n")
#         ser.flush()
#         time.sleep(1)
#         if ser.in_waiting > 0:
#             line = ser.readline().decode('utf-8').rstrip()
#             #print(line)
#             #print(line[0])
#             sys.stdout.flush()
#             if line == "STARTED":
#                 print("STARTED")
#                 sys.stdout.flush()
#                 started = True  # Exit the loop if the command is sent successfully
#                 break
#             else:
#             # Attempt to parse the data to check if it begins with 1 or 2
#                 try:
#                     first_number = int(line.split(',')[0].strip())
#                     if first_number in [1, 2, 3, 4]:
#                         print("Data collection has started with data:", line)
#                         sys.stdout.flush()
#                         started = True  # Exit the loop as data collection has started
#                 except ValueError:
#                     # Handle the case where the parsing fails (e.g., if the line doesn't contain expected data format)
#                     pass
#     except KeyboardInterrupt:
#         ser.close()
#     time.sleep(0.1)

# # Now, this is listening from the Data Collection loop on the pico
# try:
#     print("Listening for data from PICO...")
#     sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG
#     current_filename = None  # Store the current filename
#     file_opened = False  # Flags to track if file is opened
#     all_data_received = False
#     led_count = 0
#     current_error_filename = None
#     error_file_opened = False
#     intensity_exp_data = []  # List to store intensity data - For plotting

#     while True:
#         if ser.in_waiting > 0:
#             data = ser.readline().decode('utf-8').rstrip()
#             # Write data to file with timestamp in filename
#             if not file_opened:  # If no file is opened, open a new one
#                 timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#                 filename = f"data_{timestamp}.csv"
#                 filepath = os.path.join(data_directory, filename)
#                 current_filename = filepath
#                 file_opened = True  # Set the flag to indicate file is opened

#             with open(current_filename, 'a') as file:

#                 # Check if received data indicates end of 3 LED data
#                 if data == "0, 0, 0":  # Pico sends it after it is done with each LED
#                     print(f"LED {led_count + 1} done")
#                     sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG
#                     led_count += 1 # this is 4 after a full sweep 
#                     if led_count == 4: 
#                         all_data_received = True
#                         break
#                 else:
#                     file.write(data + "\n")

#     # Check if all data for 3 LEDs has been received
#     if all_data_received:
        
#         # Try to get the error log
#         while True:
#             if ser.in_waiting > 0:
#                 error = ser.readline().decode('utf-8').rstrip()
#                 # Write data to file with timestamp in filename
#                 if not error_file_opened:  # If no file is opened, open a new one
#                     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#                     filename = f"error_{timestamp}.csv"
#                     filepath = os.path.join(error_directory, filename)
#                     current_error_filename = filepath
#                     error_file_opened = True  # Set the flag to indicate file is opened

#                 with open(current_error_filename, 'a') as file:
#                     print(f"Logging error message from PICO")
#                     file.write(error + "\n")
#             else: 
#             print(f"No error messages from PICO")
#             sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG

#         # Send message back to PICO
#         print("Data received for 3 LED, sending confirmation to PICO...")
#         sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG
#         ser.write(b"DATA RECEIVED\n")
#         ser.flush()
#         # Reset LED count and flags
#         led_count = 0
#         all_data_received = False
#         file_opened = False  # Reset the flags to indicate no files are opened
#         error_file_opened = False
#         ser.close()

#         #time.sleep(0.1)
# except KeyboardInterrupt:
#     ser.close()

# #started = False
# ser.close()

import serial
import signal
import time
import os
from datetime import datetime
import sys

# Example cleanup function
def clean_exit(signum, frame):
    print("Closing the receive script...")
    sys.stdout.flush()
    # Close the serial connection here
    ser.close()
    sys.exit(0)

# Register the signal handler for clean exit
signal.signal(signal.SIGINT, clean_exit)

# Specify the directory where the files should be saved
data_directory = os.path.join(os.path.dirname(__file__), 'data')  # Data directory
error_directory = os.path.join(os.path.dirname(__file__), 'error')  # Error directory

# Create the directories if they don't exist
os.makedirs(data_directory, exist_ok=True)
os.makedirs(error_directory, exist_ok=True)

# Initialize the serial connection
uart_id = 0
baud_rate = 115200
try:
    ser = serial.Serial('/dev/tty.usbserial-A900LFQY', baud_rate, timeout=1)
except Exception as e:
    print("Error opening serial port:", e)
    sys.exit(1)

print("Running data reception script...")
sys.stdout.flush()

# Communicate with the main loop on the PICO
# This starts the data collection loop
started = False
while not started:
    try:
        print("Sending start command to PICO...")
        sys.stdout.flush()
        ser.write(b"MEASURE\n")
        ser.flush()
        time.sleep(1)
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            #print(line)
            #print(line[0])
            sys.stdout.flush()
            if line == "STARTED":
                print("STARTED")
                sys.stdout.flush()
                started = True  # Exit the loop if the command is sent successfully
                break
            else:
            # Attempt to parse the data to check if it begins with 1 or 2
                try:
                    first_number = int(line.split(',')[0].strip())
                    if first_number in [1, 2, 3, 4]:
                        print("Data collection has started with data:", line)
                        sys.stdout.flush()
                        started = True  # Exit the loop as data collection has started
                except ValueError:
                    # Handle the case where the parsing fails (e.g., if the line doesn't contain expected data format)
                    pass
    except KeyboardInterrupt:
        ser.close()
    time.sleep(0.1)

# Main data collection loop
# This is receiving data from the DataCollection.py file on the pico
# Which has now control of the UART port

try:
    print("Listening for data from PICO...")
    sys.stdout.flush()

    current_filename = None  # Store the current filename
    current_error_filename = None
    led_count = 0
    all_data_received = False
    file_opened = False
    error_file_opened = False

    while not all_data_received:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()

            # Check for the end of data for an LED
            if data == "0, 0, 0":
                print(f"LED {led_count + 1} data collection complete.")
                sys.stdout.flush()
                led_count += 1
                if led_count >= 4:  # Change this if the number of LEDs changes
                    all_data_received = True
                continue  # Do not write this line to the file

            # Open a new file on the first data received
            if not file_opened:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                current_filename = os.path.join(data_directory, f"data_{timestamp}.csv")
                file_opened = True

            # Write data to the file
            with open(current_filename, 'a') as file:
                file.write(data + "\n")
    
    # We exit this loop once all data has been received (we see "0, 0, 0" for the fourth time)
    # Now, we need to get the error log from the PICO
    while not error_log_received:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            print("data")
            sys.stdout.flush()
            # Check for the end of data for an LED
            if data == "DONE":
                print(f"Error log received")
                sys.stdout.flush()
                error_log_received = True
            continue # Do not write this line to the file

            # Open a new file on the first data received
            if not file_opened:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                current_error_filename = os.path.join(error_directory, f"error_log_{timestamp}.csv")
                error_file_opened = True

            # Write data to the file
            with open(current_error_filename, 'a') as file:
                file.write(data + "\n")

    # Send confirmation of reception of data back to PICO
    print("All LED data and error log received, sending confirmation to PICO...")
    sys.stdout.flush()
    time.sleep(3)
    ser.write(b"RECEIVED\n")
    ser.flush()
    # n = 5
    # while(n > 0):
    #     ser.write(b"RECEIVED\n")
    #     ser.flush()
    #     time.sleep(1)
    #     n -= 1

    # Reset the flags and counters
    led_count = 0
    all_data_received = False
    file_opened = False
    error_file_opened = False

    # Process error messages from PICO if needed (TBD)

except KeyboardInterrupt:
    print("Script interrupted by user")
    sys.stdout.flush()
finally:
    if ser.is_open:
        ser.close()

