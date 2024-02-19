import sys
sys.path.append('/opt/homebrew/lib/python3.11/site-packages')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the range of wavelengths for the experimental data
min_wavelength_exp = 910
max_wavelength_exp = 1370

# Read the experimental data
experimental_data = pd.read_csv('data/plastic_data_1050_counterclockwise_2024-02-18_13-36-52.csv')
intensity_exp = experimental_data.iloc[:, 2]  # Assuming normalized intensity is in the THIRD column (0, 1, 2)

# Map experimental data indices to the wavelength range
num_points_exp = len(experimental_data)
wavelengths_exp = np.linspace(min_wavelength_exp, max_wavelength_exp, num_points_exp)

# Smooth the experimental data (using a simple moving average for demonstration)
window_size = 10
smoothed_intensity_exp = intensity_exp.rolling(window=window_size, center=True).mean()

# Normalize the smoothed intensity data
normalized_intensity_exp = (smoothed_intensity_exp - smoothed_intensity_exp.min()) / (smoothed_intensity_exp.max() - smoothed_intensity_exp.min())

# Read the LED Spectrum data
spectrum_data = pd.read_csv('/Users/lola/Desktop/CU/CAPSTONE23-24/1050_spectrum.csv')
wavelengths_model = spectrum_data.iloc[:, 1] - 13  # Wavelengths are in the second column, adjusting by -13
intensity_model = spectrum_data.iloc[:, 0]  # Intensity is in the first column

# Interpolate the smoothed experimental data to match the model data wavelengths
interpolated_intensity_exp = np.interp(wavelengths_model, wavelengths_exp, normalized_intensity_exp)

# Plot: Experimental Data and LED Model Spectrum
plt.figure(figsize=(10, 8))
plt.plot(wavelengths_model, interpolated_intensity_exp, 'b', label='Interpolated Experimental Data')
plt.plot(wavelengths_model, intensity_model, 'r', label='LED Model Spectrum')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Intensity')
plt.title('Experimental Data and LED Model Spectrum')
plt.legend(loc='upper left')
plt.grid(True)

plt.tight_layout()  # Adjust layout to not overlap
plt.savefig('simple_spectrum_plot.png')
plt.show()
