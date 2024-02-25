# import sys
# sys.path.append('/opt/homebrew/lib/python3.11/site-packages')
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

import serial
import time
import os
from datetime import datetime

# Specify the directory where the files should be saved
data_directory = os.path.join(os.path.dirname(__file__), 'data')  # Assuming this script is in the DATA_PROCESSING directory

# Create the data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Replace 'COM_PORT' with your device file '/dev/tty.usbserial-A900LFQY'
uart_id = 0
baud_rate = 115200
print("running script...")
try: 
    ser = serial.Serial('/dev/tty.usbserial-A900LFQY', baud_rate, timeout=1)
except FileNotFoundError:
    print("UART adapter not found at its expected location")
    

# # PLOTTING STUFF 
# # Define the range of wavelengths for the experimental data
# min_wavelength_exp = 910
# max_wavelength_exp = 1370

# # Function to plot the data
# def plot_data(intensity_exp):
#     # Smooth the experimental data (using a simple moving average for demonstration)
#     window_size = 10
#     smoothed_intensity_exp = pd.Series(intensity_exp).rolling(window=window_size, center=True).mean()

#     # Normalize the smoothed intensity data
#     normalized_intensity_exp = (smoothed_intensity_exp - smoothed_intensity_exp.min()) / (smoothed_intensity_exp.max() - smoothed_intensity_exp.min())

#     # Map experimental data indices to the wavelength range
#     num_points_exp = len(normalized_intensity_exp)
#     wavelengths_exp = np.linspace(min_wavelength_exp, max_wavelength_exp, num_points_exp)

#     # Plot: Experimental Data
#     plt.figure(figsize=(10, 8))
#     plt.plot(wavelengths_exp, normalized_intensity_exp, 'b', label='Normalized Experimental Data')
#     plt.xlabel('Wavelength (nm)')
#     plt.ylabel('Normalized Intensity')
#     plt.title('Real-time Plot of Experimental Data')
#     plt.legend(loc='upper left')
#     plt.grid(True)
#     plt.tight_layout()  # Adjust layout to not overlap
#     plt.draw()
#     plt.pause(0.1)  # Pause to allow the plot to be updated

# # END OF PLOTTING STUFF

# Call the main function

try:
    print("listening for data from PICO...")
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
                filename = f"phone_flashlight_data_1200_{direction}_{timestamp}.csv"
                filepath = os.path.join(data_directory, filename)
                current_filenames[led_count] = filepath
                file_opened[led_count] = True  # Set the flag to indicate file is opened
            
            # ============== PLOTTING STUFF

            # # Append intensity data to the list
            # intensity_exp_data.append(data)

            # # Check if a certain number of data points have been received
            # if len(intensity_exp_data) == 10:  # Change this number as needed
            #     plot_data(intensity_exp_data)
            #     intensity_exp_data.clear()  # Clear intensity data for the next set of points
            
            # ============== END PLOTTING STUFF

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
