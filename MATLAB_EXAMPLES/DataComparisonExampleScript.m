% Load data from the first text file
data1 = readtable('/Users/lola/Desktop/CU/CAPSTONE23-24/MATLAB_EXAMPLES/refl-VNIR_H2O_ice_70micron_70K_abg.data.txt');

% Extract data for plotting from the first dataset
wavelength1 = data1.wavelength_nm_; % Replace with the correct column name if different
reflectance1 = data1.reflectance_factor; % Replace with the correct column name if different

% Load model data
data2 = readtable('/Users/lola/Desktop/CU/CAPSTONE23-24/MATLAB_EXAMPLES/refl-VNIR_H2O_ice_mix_77pc70micron_23pc1060micron_140K_abg.data.txt'); % Update with the actual file path

% Extract data for plotting from the second dataset
wavelength2 = data2.wavelength_nm_; % Replace with the correct column name if different
reflectance2 = data2.reflectance_factor; % Replace with the correct column name if different

% Plot the data from both datasets
figure;
plot(wavelength1, reflectance1, 'b-', 'LineWidth', 1.5); % First dataset in blue
hold on; % Hold on to add another plot to the same figure
plot(wavelength2, reflectance2, 'r-', 'LineWidth', 1.5); % Second dataset in red
hold off; % Release the plot hold

xlabel('Wavelength (nm)');
ylabel('Reflectance Factor');
title('Comparison of Reflectance Factors as a Function of Wavelength');
legend('Dataset 1', 'Model Data'); % Add a legend to distinguish the datasets
grid on;