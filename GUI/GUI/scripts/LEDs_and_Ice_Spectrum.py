import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import sys

# Filenames of the CSV files
#csv_filenames = ['/Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/data/LED_spectrum_data/1050_spectrum.csv', '/Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/data/LED_spectrum_data/1200_spectrum.csv', '/Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/data/LED_spectrum_data/1550_spectrum.csv']
csv_filenames = ['/Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/data/LED_spectrum_data/all_LEDs_spectrum.csv']

# Load and concatenate the data from the CSV files
dataframes = [pd.read_csv(filename) for filename in csv_filenames]
data = pd.concat(dataframes, ignore_index=True)

ice_data = pd.read_csv('/Users/lola/Desktop/CU/CAPSTONE23-24/EXPERIMENT_OP_20201223_001/refl-VNIR_H2O_ice_70micron_70K/refl-VNIR_H2O_ice_70micron_70K_abg.data.csv')

# Prepare the figure for plotting
# fig, ax = plt.subplots()
# line, = ax.plot([], [], lw=2)

# Setting the axes limits
#ax.set_xlim(data.iloc[:, 1].min(), data.iloc[:, 1].max())

# Prepare the figure for plotting with two subplots
fig, (ax_ice, ax) = plt.subplots(2, 1, sharex=True)
ax.set_xlim(850, 1800)
ax.set_ylim(data.iloc[:, 0].min(), data.iloc[:, 0].max())

# Plot the ice data on the first subplot (ax_ice)
ax_ice.plot(ice_data['wavelength(nm)'], ice_data['reflectance_factor'], color='blue', label='Ice Data')
ax_ice.legend()
ax_ice.set_ylabel('Reflectance Factor')
ax_ice.set_title('Ice Data')
ax_ice.set_xlim(850, 1800)  # Set the x-axis range from 850 to 1600 nm

# Plot the LED data on the second subplot (ax_led)
ax.plot(data.iloc[:, 1], data.iloc[:, 0], color='red', label='LEDs specs')
ax.legend()
ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('Intensity')
ax.set_title('LED Data')

# Adjust the spacing between the plots
plt.tight_layout()

# Show the plots
plt.show()