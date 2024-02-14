# import serial
# import time
# import os
# from datetime import datetime

# # Replace 'COM_PORT' with your device file '/dev/tty.usbserial-A900LFQY'
# uart_id = 0
# baud_rate = 115200
# ser = serial.Serial('/dev/tty.usbserial-A900LFQY', baud_rate, timeout=1)

# # Call the main function

# try:
#     current_filename = None  # Store the current filename
#     file_opened = False  # Flag to track if a file is opened
#     all_data_received = False
#     led_count = 0
    
#     while True:
#         if ser.in_waiting > 0:
#             data = ser.readline().decode('utf-8').rstrip()
#             # Write data to file with timestamp in filename
#             if not file_opened:  # If no file is opened, open a new one
#                 timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#                 current_filename = f"air_data_{timestamp}.csv"
#                 file_opened = True  # Set the flag to indicate file is opened
#             with open(current_filename, 'a') as file:
#                 file.write(data + "\n")

#             # Check if received data indicates end of 3 LED data
#             if data == "0, 0, 0":  # Pico sends it after it is done with each LED
#                 led_count += 1
#                 print(f"LED {led_count} done")
#                 if led_count == 2: ## TODO: FOR TESTING WITH 1 LED, DOUBLE SWEEP. Eventally, change back to 3
#                     all_data_received = True

#         # Check if all data for 3 LEDs has been received
#         if all_data_received:
#             # Send message back to PICO
#             print("Data received for 3 LED, sending confirmation to PICO...")
#             ser.write(b"DATA RECEIVED\n")

#             # Reset LED count and flag
#             led_count = 0
#             all_data_received = False
#             file_opened = False  # Reset the flag to indicate no file is opened

#         #time.sleep(0.1)
# except KeyboardInterrupt:
#     ser.close()

import serial
import time
import os
from datetime import datetime

# Replace 'COM_PORT' with your device file '/dev/tty.usbserial-A900LFQY'
uart_id = 0
baud_rate = 115200
ser = serial.Serial('/dev/tty.usbserial-A900LFQY', baud_rate, timeout=1)

# Call the main function

try:
    current_filenames = [None, None]  # Store the current filenames for clockwise and counterclockwise
    file_opened = [False, False]  # Flags to track if files are opened for clockwise and counterclockwise
    all_data_received = False
    led_count = 0
    
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            # Write data to file with timestamp in filename
            if not file_opened[led_count]:  # If no file is opened, open a new one
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                direction = "clockwise" if led_count == 0 else "counterclockwise"
                current_filenames[led_count] = f"air_data_{direction}_{timestamp}.csv"
                file_opened[led_count] = True  # Set the flag to indicate file is opened
            with open(current_filenames[led_count], 'a') as file:

                # Check if received data indicates end of 3 LED data
                if data == "0, 0, 0":  # Pico sends it after it is done with each LED
                    print(f"LED {led_count + 1} done")
                    led_count += 1
                    if led_count == 2: ## TODO: FOR TESTING WITH 1 LED, DOUBLE SWEEP. Eventally, change back to 3
                        all_data_received = True
                else:
                    file.write(data + "\n")

        # Check if all data for 3 LEDs has been received
        if all_data_received:
            # Send message back to PICO
            print("Data received for 3 LED, sending confirmation to PICO...")
            ser.write(b"DATA RECEIVED\n")

            # Reset LED count and flags
            led_count = 0
            all_data_received = False
            file_opened = [False, False]  # Reset the flags to indicate no files are opened

        #time.sleep(0.1)
except KeyboardInterrupt:
    ser.close()
