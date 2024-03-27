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
    # Close your serial connection here
    ser.close()
    sys.exit(0)

# Register the signal handler for clean exit
signal.signal(signal.SIGINT, clean_exit)

# Specify the directory where the files should be saved
data_directory = os.path.join(os.path.dirname(__file__), 'data')  # Assuming this script is in the DATA_PROCESSING directory

# Create the data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Replace 'COM_PORT' with your device file '/dev/tty.usbserial-A900LFQY'
uart_id = 0
baud_rate = 115200
print("Running data reception script...")
sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG
try: 
    ser = serial.Serial('/dev/tty.usbserial-A900LFQY', baud_rate, timeout=1)
except FileNotFoundError:
    print("UART adapter not found at its expected location")
    sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG
    

# Call the main function
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
                    if first_number in [1, 2]:
                        print("Data collection has started with data:", line)
                        sys.stdout.flush()
                        started = True  # Exit the loop as data collection has started
                except ValueError:
                    # Handle the case where the parsing fails (e.g., if the line doesn't contain expected data format)
                    pass
    except KeyboardInterrupt:
        ser.close()
    time.sleep(0.1)    

# Now, this is listening from the Data Collection loop on the pico
try:
    print("Listening for data from PICO...")
    sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG
    current_filenames = [None, None]  # Store the current filenames for clockwise and counterclockwise
    file_opened = [False, False]  # Flags to track if files are opened for clockwise and counterclockwise
    all_data_received = False
    led_count = 0
    intensity_exp_data = []  # List to store intensity data - For plotting
    
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            # Write data to file with timestamp in filename
            if not file_opened[led_count]:  # If no file is opened, open a new one
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                direction = "clockwise" if led_count == 0 else "counterclockwise"
                filename = f"data_{direction}_{timestamp}.csv"
                filepath = os.path.join(data_directory, filename)
                current_filenames[led_count] = filepath
                file_opened[led_count] = True  # Set the flag to indicate file is opened

            with open(current_filenames[led_count], 'a') as file:

                # Check if received data indicates end of 3 LED data
                if data == "0, 0, 0":  # Pico sends it after it is done with each LED
                    print(f"LED {led_count + 1} done")
                    sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG 
                    led_count += 1
                    if led_count == 2: ## TODO: FOR TESTING WITH 1 LED, DOUBLE SWEEP. Eventally, change back to 3
                        all_data_received = True
                else:
                    file.write(data + "\n")

        # Check if all data for 3 LEDs has been received
        if all_data_received:
            # Send message back to PICO
            print("Data received for 3 LED, sending confirmation to PICO...")
            sys.stdout.flush() # ADD THIS AFTER ANY PRINT STATEMENT TO AVOID A BUFFER TOO BIG
            ser.write(b"DATA RECEIVED\n")
            ser.flush()
            # Reset LED count and flags
            led_count = 0
            all_data_received = False
            file_opened = [False, False]  # Reset the flags to indicate no files are opened
            ser.close()

        #time.sleep(0.1)
except KeyboardInterrupt:
    ser.close()

#started = False
ser.close()

