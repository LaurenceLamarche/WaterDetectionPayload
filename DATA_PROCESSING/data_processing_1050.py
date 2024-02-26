# import pandas as pd
# import matplotlib.pyplot as plt

# # Read data from CSV files

# # Read the LED Spectrum data (needed to extrapolate the wavelengths on graph)
# spectrum_data = pd.read_csv('data/LED_spectrum_data/1050_spectrum.csv')
# wavelengths_model = spectrum_data.iloc[:, 1] - 13  # Wavelengths are in the second column, adjusting by -13
# intensity_model = spectrum_data.iloc[:, 0]  # Intensity is in the first column

# # EXPERIMENTAL DATA FOR 1050 LED 1
# air_data = pd.read_csv('data/air_data_1050_counterclockwise_2024-02-18_13-29-27.csv')
# plastic_data = pd.read_csv('data/plastic_data_1050_counterclockwise_2024-02-18_13-36-52.csv')
# water_data = pd.read_csv('data/water_data_1050_counterclockwise_2024-02-18_13-44-29.csv')

# # transforming experimental data to the right wavelength
# original_min = air_data.iloc[:, 1].min()
# original_max = air_data.iloc[:, 1].max()
# desired_min = 780
# desired_max = 1300

# air_data.iloc[:, 1] = ((air_data.iloc[:, 1] - original_min) / (original_max - original_min)) * (desired_max - desired_min) + desired_min
# plastic_data.iloc[:, 1] = ((plastic_data.iloc[:, 1] - original_min) / (original_max - original_min)) * (desired_max - desired_min) + desired_min
# water_data.iloc[:, 1] = ((water_data.iloc[:, 1] - original_min) / (original_max - original_min)) * (desired_max - desired_min) + desired_min

# # READ CHOSEN THEORETICAL DATA FOR COMPARISON ON SECOND PLOT
# # model_water_liquid_spectrum = pd.read_csv('model_water_liquid_spectrum.csv') # we are yet to find good data for this one
# model_water_vapor_spectrum = pd.read_csv('data/Theoretical_water_data/model_water_vapor_spectrum.csv')
# model_water_vapor_spectrum.iloc[:, 0] = 1 / (model_water_vapor_spectrum.iloc[:, 0] * 1e-7)

# # Create figure and axes for subplots
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# # Plot experimental data in the first subplot
# ax1.plot(air_data.iloc[:, 1], air_data.iloc[:, 2], label='air')
# ax1.plot(plastic_data.iloc[:, 1], plastic_data.iloc[:, 2], label='plastic bag')
# ax1.plot(water_data.iloc[:, 1], water_data.iloc[:, 2], label='plastic bag with water')
# ax1.plot(wavelengths_model, intensity_model, label='1050 LED spectrum data')
# ax1.set_xlabel('Wavelength')
# ax1.set_ylabel('Intensity')
# ax1.set_title('Intensity vs Wavelength')
# ax1.legend()

# # Plot water-plastic and theoretical curves in the second subplot
# water_minus_plastic = water_data.iloc[:, 2] - plastic_data.iloc[:, 2]
# ax2.plot(water_data.iloc[:, 1], water_minus_plastic, label='water minus plastic')
# #ax2.plot(model_water_liquid_spectrum['Wavelength'], model_water_liquid_spectrum['Intensity'], label='liquid water absorption spectrum')
# #ax2.plot(model_water_vapor_spectrum.iloc[:, 0], model_water_vapor_spectrum.iloc[:, 1], label='water vapor absorption spectrum')
# ax2.set_xlabel('Wavelength')
# ax2.set_ylabel('Intensity')
# ax2.set_title('Absorption Spectra')
# ax2.legend()

# # Adjust layout to prevent overlap
# plt.tight_layout()

# # Show plot
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV files

# Read the LED Spectrum data (needed to extrapolate the wavelengths on graph)
spectrum_data = pd.read_csv('data/LED_spectrum_data/1050_spectrum.csv')
wavelengths_model = spectrum_data.iloc[:, 1] - 13  # Wavelengths are in the second column, adjusting by -13
intensity_model = spectrum_data.iloc[:, 0]  # Intensity is in the first column

# EXPERIMENTAL DATA FOR 1050 LED 1
air_data = pd.read_csv('data/air_data_1050_counterclockwise_2024-02-18_13-29-27.csv')
plastic_data = pd.read_csv('data/plastic_data_1050_counterclockwise_2024-02-18_13-36-52.csv')
water_data = pd.read_csv('data/water_data_1050_counterclockwise_2024-02-18_13-44-29.csv')

# transforming experimental data to the right wavelength
original_min = air_data.iloc[:, 1].min()
original_max = air_data.iloc[:, 1].max()
desired_min = 780
desired_max = 1300

air_data.iloc[:, 1] = ((air_data.iloc[:, 1] - original_min) / (original_max - original_min)) * (desired_max - desired_min) + desired_min
plastic_data.iloc[:, 1] = ((plastic_data.iloc[:, 1] - original_min) / (original_max - original_min)) * (desired_max - desired_min) + desired_min
water_data.iloc[:, 1] = ((water_data.iloc[:, 1] - original_min) / (original_max - original_min)) * (desired_max - desired_min) + desired_min

# READ CHOSEN THEORETICAL DATA FOR COMPARISON ON SECOND PLOT
# model_water_liquid_spectrum = pd.read_csv('model_water_liquid_spectrum.csv') # we are yet to find good data for this one
model_water_vapor_spectrum = pd.read_csv('data/Theoretical_water_data/model_water_vapor_spectrum.csv')
model_water_vapor_spectrum.iloc[:, 0] = 1 / (model_water_vapor_spectrum.iloc[:, 0] * 1e-7)

# Create figure and axes for subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)  # Use sharex parameter to align x-axis scales

# Plot experimental data in the first subplot
ax1.plot(air_data.iloc[:, 1], air_data.iloc[:, 2], label='air')
ax1.plot(plastic_data.iloc[:, 1], plastic_data.iloc[:, 2], label='plastic bag')
ax1.plot(water_data.iloc[:, 1], water_data.iloc[:, 2], label='plastic bag with water')
ax1.plot(wavelengths_model, intensity_model, label='1050 LED spectrum data')
ax1.set_xlabel('Wavelength')
ax1.set_ylabel('Intensity')
ax1.set_title('Intensity vs Wavelength')
ax1.legend()

# Plot water-plastic and theoretical curves in the second subplot
water_minus_plastic = water_data.iloc[:, 2] - plastic_data.iloc[:, 2]
ax2.plot(water_data.iloc[:, 1], water_minus_plastic, label='water minus plastic')
#ax2.plot(model_water_liquid_spectrum['Wavelength'], model_water_liquid_spectrum['Intensity'], label='liquid water absorption spectrum')
#ax2.plot(model_water_vapor_spectrum.iloc[:, 0], model_water_vapor_spectrum.iloc[:, 1], label='water vapor absorption spectrum')
ax2.set_xlabel('Wavelength')
ax2.set_ylabel('Intensity')
ax2.set_title('Absorption Spectra')
ax2.legend()

# Adjust layout to prevent overlap
plt.tight_layout()

# Show plot
plt.show()

