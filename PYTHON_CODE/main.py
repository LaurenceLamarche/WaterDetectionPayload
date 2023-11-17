import machine
import time
import uos
from Motor import Motor

class PayloadFlightControl:

    def __init__(self):
        # Initialize Motor instance
        self.motor = Motor()
        # Set up any other initializations if necessary

    # Function to combine sensor readings into a single data packet
    def combine_sensor_readings(self):
        # Read sensor values
        # TODO: replace with actual real function from DataCollection.py
        # combined_data = f"{photodetector_value},{motor_angle},{temperature_1},{temperature_2}"
        
        return "65535,32768,1023,512"

    def start_collection(self):
        # TODO: this loop should start data collection. 
            # Open (or create) a file to store the data
        with open('sensor_data.txt', 'w') as file:
            for loop_number in range(1, 4):  # Outer loop, runs three times
                for step_count in range(4000):  # Inner loop, runs 4000 times for each outer loop
                    # Get combined sensor reading
                    combined_data = self.combine_sensor_readings()

                    # Append the loop number to the data
                    data_to_write = f"{loop_number},{combined_data}\n"

                    # Write the data to the file
                    file.write(data_to_write)

                    # Change motor angle here
                    # Assuming 'perform_steps' changes the motor angle and 'num_steps' is the number of steps for desired angle change

                    # TODO: the motor needs to move here after we collected the data
                    self.motor.move(1000, 120)  # Move 1000 steps in 120 seconds
                    
                # Optional: a small delay between each outer loop iteration
                time.sleep(1)
                # TODO: call the calibration algorithm HERE
            
        print("One full sample complete for all LEDs. Data stored in 'sensor_data.txt'.")

def main():
    # TODO: this loop should listen for ground commands, and either 
    # START DATA COLLECTION
    # STOP DATA COLLECTION
    # FORCE CALIBRATE
    # GET DATA

    print("This is the main loop")

# Call the main function
if __name__ == "__main__":
    main()