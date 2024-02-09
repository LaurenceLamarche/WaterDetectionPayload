import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the range of wavelengths for the experimental data
min_wavelength_exp = 1337
max_wavelength_exp = 1627

# Define the wavelength range to display for the water ice model data
lower_bound = 1204
upper_bound = 1792

# Read the experimental data
experimental_data = pd.read_csv('/Users/lola/Desktop/CU/CAPSTONE23-24/datasweep 1550 led with cap.csv')
intensity_exp = experimental_data.iloc[:, 1]  # Assuming normalized intensity is in the second column

# Map experimental data indices to the wavelength range
num_points_exp = len(experimental_data)
wavelengths_exp = np.linspace(min_wavelength_exp, max_wavelength_exp, num_points_exp)

# Smooth the experimental data (using a simple moving average for demonstration)
window_size = 10
smoothed_intensity_exp = intensity_exp.rolling(window=window_size, center=True).mean()

# Normalize the smoothed intensity data
normalized_intensity_exp = (smoothed_intensity_exp - smoothed_intensity_exp.min()) / (smoothed_intensity_exp.max() - smoothed_intensity_exp.min())

# Read the LED Spectrum data
spectrum_data = pd.read_csv('/Users/lola/Desktop/CU/CAPSTONE23-24/1550_spectrum_correct.csv')
wavelengths_model = spectrum_data.iloc[:, 1] - 13  # Wavelengths are in the second column, adjusting by -13
intensity_model = spectrum_data.iloc[:, 0]  # Intensity is in the first column

# Interpolate the smoothed experimental data to match the model data wavelengths
interpolated_intensity_exp = np.interp(wavelengths_model, wavelengths_exp, normalized_intensity_exp)

# Plot 1: Experimental Data and LED Model Spectrum
plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)  # Divide figure into 2 rows, 1 column, activate first area
plt.plot(wavelengths_model, interpolated_intensity_exp, 'b', label='Interpolated Experimental Data')
plt.plot(wavelengths_model, intensity_model, 'r', label='LED Model Spectrum')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Intensity')
plt.title('Experimental Data and LED Model Spectrum')
plt.legend(loc='upper left')
plt.grid(True)

# Read the H2O ice model data
water_ice_data = pd.read_csv('/Users/lola/Desktop/CU/CAPSTONE23-24/EXPERIMENT_OP_20201223_001/refl-VNIR_H2O_ice_70micron_70K/refl-VNIR_H2O_ice_70micron_70K_abg.data.csv', header=0)
wavelength1 = water_ice_data.iloc[:, 0]
reflectance1 = water_ice_data.iloc[:, 1]

# Filter the data to include only the wavelengths within the specified range
filter_indices = (wavelength1 >= lower_bound) & (wavelength1 <= upper_bound)
filtered_wavelength = wavelength1[filter_indices]
filtered_reflectance = reflectance1[filter_indices]

# Plot 2: Water Ice Data and Isolated Spectrum
plt.subplot(2, 1, 2)  # Activate second area
plt.plot(filtered_wavelength, filtered_reflectance, color=[1, 0.6471, 0], linewidth=2, label='Water Ice Data')
isolated_spectrum = interpolated_intensity_exp - intensity_model  # Subtract the model spectrum
plt.plot(wavelengths_model, isolated_spectrum, color=[0, 0.5, 0], linewidth=1.5, label='Isolated Spectrum')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Intensity')
plt.title('Water Ice Data and Isolated Spectrum')
plt.legend(loc='lower left')
plt.grid(True)

plt.tight_layout()  # Adjust layout to not overlap
plt.savefig('1550_spectrum_two_plots.png')
plt.show()
