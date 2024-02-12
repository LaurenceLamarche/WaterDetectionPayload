import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

# Clear existing figures
plt.clf()

# Define the range of wavelengths for the experimental data
min_wavelength_exp_model = 815
max_wavelength_exp_model = 1115

# Read the model (air) experimental data
experimental_model_data = pd.read_csv('/Users/lola/Desktop/CU/CAPSTONE23-24/spectrum_Feb9_1050_trial2.csv')
intensity_exp_model = experimental_model_data.iloc[:, 1].values  # Assuming normalized intensity is in the second column
# Map experimental data indices to the wavelength range
num_points_exp_model = len(experimental_model_data)
wavelengths_exp_model = np.linspace(min_wavelength_exp_model, max_wavelength_exp_model, num_points_exp_model)
# Smooth the experimental data
smoothed_intensity_exp_model = savgol_filter(intensity_exp_model, 11, 3)  # window size 11, polynomial order 3
# Normalize the smoothed intensity data
normalized_intensity_exp_model = (smoothed_intensity_exp_model - min(smoothed_intensity_exp_model)) / (max(smoothed_intensity_exp_model) - min(smoothed_intensity_exp_model))

# Define the range of wavelengths for the experimental (water) data
min_wavelength_exp = 950
max_wavelength_exp = 1075

# Read the water experimental data
experimental_data = pd.read_csv('/Users/lola/Desktop/CU/CAPSTONE23-24/spectrum_Feb9_1050_water.csv')
intensity_exp = experimental_data.iloc[:, 1].values  # Assuming normalized intensity is in the second column
# Map experimental data indices to the wavelength range
num_points_exp = len(experimental_data)
wavelengths_exp = np.linspace(min_wavelength_exp, max_wavelength_exp, num_points_exp)
# Smooth the experimental data
smoothed_intensity_exp = savgol_filter(intensity_exp, 11, 3)  # window size 11, polynomial order 3
# Normalize the smoothed intensity data
normalized_intensity_exp = (smoothed_intensity_exp - min(smoothed_intensity_exp)) / (max(smoothed_intensity_exp) - min(smoothed_intensity_exp))

# Read the LED Spectrum data
spectrum_data = pd.read_csv('/Users/lola/Desktop/CU/CAPSTONE23-24/1050_spectrum.csv')
wavelengths_model = spectrum_data.iloc[:, 1].values  # Wavelengths are in the second column
intensity_model = spectrum_data.iloc[:, 0].values  # Intensity is in the first column

# Interpolate the smoothed experimental model (air) data to match the model data wavelengths
interpolator_exp_model = interp1d(wavelengths_exp_model, normalized_intensity_exp_model, kind='linear')
interpolated_intensity_exp_model = interpolator_exp_model(wavelengths_model)

# Interpolate the smoothed experimental water data to match the model data wavelengths
interpolator_exp = interp1d(wavelengths_exp, normalized_intensity_exp, kind='linear')
interpolated_intensity_exp = interpolator_exp(wavelengths_model)

# Plot 1: Experimental Data and LED Model Spectrum
plt.subplot(3, 1, 1)
plt.plot(wavelengths_model, interpolated_intensity_exp, 'b', label='Interpolated Experimental Data (Water)')
plt.plot(wavelengths_model, intensity_model, 'r', label='LED Model Spectrum')
plt.plot(wavelengths_model, interpolated_intensity_exp_model, 'g', label='Interpolated Experimental Data (Air)')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Intensity')
plt.title('Experimental Data and LED Model Spectrum')
plt.legend(loc='upper left')
plt.grid(True)

# Plot 2: Water Vapor Data and Isolated Spectrum
plt.subplot(3, 1, 2)
isolated_spectrum_exp = interpolated_intensity_exp - interpolated_intensity_exp_model
isolated_spectrum_LED = interpolated_intensity_exp - intensity_model
plt.plot(wavelengths_model, isolated_spectrum_exp, color=[1, 0.6471, 0], linewidth=2, label='Water Spectrum (- Exp. Data)')
plt.plot(wavelengths_model, isolated_spectrum_LED, color=[0, 0.5, 0], linewidth=1.5, label='Water Spectrum (- LED Model)')
plt.xlim([950, 1100])
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Intensity')
plt.title('Water Experimental Data, Isolated Spectrum')
plt.legend(loc='upper left')
plt.grid(True)

# Plot 3: Water Experimental Data, Isolated Spectrum (Log Scale)
plt.subplot(3, 1, 3)
plt.semilogx(wavelengths_model, isolated_spectrum_exp, color=[1, 0.6471, 0], linewidth=2, label='Water Spectrum (- Exp. Data)')
plt.semilogx(wavelengths_model, isolated_spectrum_LED, color=[0, 0.5, 0], linewidth=1.5, label='Water Spectrum (- LED Model)')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Intensity')
plt.title('Water Vapor Data and Isolated Spectrum (Log X Scale)')
plt.legend(loc='upper left')
plt.grid(True)

# Save and display the figure

# Get current timestamp
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Construct the file path for saving the plot
# Assuming the script is in DATA_PROCESSING/1050_data_processing.py
# and you want to save the plots in DATA_PROCESSING/plots/
plot_directory = 'plots'  # Relative path to the plots directory
script_directory = os.path.dirname(__file__)  # Gets the directory of the current script
plots_path = os.path.join(script_directory, plot_directory)  # Full path to the plots directory

# Ensure the plots directory exists, if not, create it
if not os.path.exists(plots_path):
    os.makedirs(plots_path)

# Construct the full path for the output file, including the timestamp
output_file_name = f'1050_spectrum_log_scale_{timestamp}.png'
output_file_path = os.path.join(plots_path, output_file_name)

# Plotting code remains the same

# Save the figure with the constructed path
plt.savefig(output_file_path)
plt.show()
