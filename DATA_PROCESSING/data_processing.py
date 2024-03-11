# import os
# import glob
# import pandas as pd
# import matplotlib.pyplot as plt

# # Directory where the data files are located
# data_directory = "/Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/data"

# # Get a list of all CSV files in the directory
# csv_files = glob.glob(os.path.join(data_directory, "*.csv"))

# # Sort the files by modification time (most recent first)
# csv_files.sort(key=os.path.getmtime, reverse=True)

# # Keep only the most recent two files
# latest_files = csv_files[:2]

# # Plot the data from the two files
# for file in latest_files:
#     try:
#         # Read the CSV file into a pandas DataFrame
#         # Since the file doesn't have column labels, provide the column names explicitly
#         df = pd.read_csv(file, header=None, usecols=[1, 2], names=['Wavelength', 'Intensity'])

#         # Apply a 10-point moving average to the intensity data
#         df['Intensity'] = df['Intensity'].rolling(window=10, min_periods=1).mean()
        
#         # Plot the data
#         plt.plot(df['Wavelength'], df['Intensity'], label=os.path.basename(file))
        
#         # Print the name of the file being plotted
#         print(f"Plotting data from file: {os.path.basename(file)}")
#     except pd.errors.ParserError as e:
#         print(f"Error processing file {file}: {e}")

# # Add labels and legend
# plt.xlabel('Wavelength')
# plt.ylabel('Intensity')
# plt.title('Latest Data Plot')
# plt.legend()

# # Show the plot
# plt.show()

import os
import glob
import argparse
import pandas as pd
import matplotlib.pyplot as plt

# Example cleanup function
def clean_exit(signum, frame):
    print("Closing the sleep script...")
    sys.stdout.flush()
    # Close your serial connection here
    ser.close()
    sys.exit(0)

# Register the signal handler for clean exit
signal.signal(signal.SIGINT, clean_exit)

def plot_latest_data(files_to_plot):
    # Directory where the data files are located
    data_directory = "/Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/data"

    # Get a list of all CSV files in the directory
    csv_files = glob.glob(os.path.join(data_directory, "*.csv"))

    # Sort the files by modification time (most recent first)
    csv_files.sort(key=os.path.getmtime, reverse=True)

    # Keep only the most recent file(s) based on the argument provided
    latest_files = csv_files[:files_to_plot]

    # Plot the data from the selected files
    for file in latest_files:
        try:
            # Read the CSV file into a pandas DataFrame
            # Since the file doesn't have column labels, provide the column names explicitly
            df = pd.read_csv(file, header=None, usecols=[1, 2], names=['Wavelength', 'Intensity'])
            
            # Apply a 10-point moving average to the intensity data
            #df['Intensity'] = df['Intensity'].rolling(window=10, min_periods=1).mean()
            
            # Plot the data
            plt.plot(df['Wavelength'], df['Intensity'], label=os.path.basename(file))
            
            # Print the name of the file being plotted
            print(f"Plotting data from file: {os.path.basename(file)}")
        except pd.errors.ParserError as e:
            print(f"Error processing file {file}: {e}")

    # Add labels and legend
    plt.xlabel('Wavelength')
    plt.ylabel('Intensity')
    plt.title('Latest Data Plot with 10-Point Moving Average')
    plt.legend()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot latest data files.')
    parser.add_argument('--files', type=int, choices=[1, 2], default=1,
                        help='Number of latest data files to plot (1 or 2)')

    args = parser.parse_args()
    plot_latest_data(args.files)

