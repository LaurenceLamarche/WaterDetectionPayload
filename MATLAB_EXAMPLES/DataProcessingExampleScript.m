
% Load data from a text file with column headers
data = readtable('/Users/lola/Desktop/CU/CAPSTONE23-24/MATLAB_EXAMPLES/refl-VNIR_H2O_ice_70micron_70K_abg.data.txt');

% Extract data for plotting
wavelength = data.wavelength_nm_; % Replace with the correct column name if different
reflectance = data.reflectance_factor; % Replace with the correct column name if different

% Plot the data
figure;
plot(wavelength, reflectance, 'b-', 'LineWidth', 1.5); % 'b-' sets the line color to blue
xlabel('Wavelength (nm)');
ylabel('Reflectance Factor');
title('Reflectance Factor as a Function of Wavelength');
grid on;