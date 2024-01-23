import machine
import time
import uos
from Motor import Motor

class DataCollection:

    def __init__(self):
        # Initialize Motor instance
        self.motor = Motor()
        # self.motor = [] # TESTING ON VS CODE
        # Set up any other initializations if necessary
        # TODO: integrate the Pi communicator class (or something) for code that calls other pico
        # TODO: integrate the LEDcommunicator class (or something) for code that controls LEDs 
        #       (that might be done in PiCommunicator class)


    # Function to combine sensor readings into a single data packet
    def combine_sensor_readings(self):
        # Read sensor values
        # TODO: replace with actual real functions from DataCollectionTest.py
        # combined_data = f"{photodetector_value},{motor_angle},{temperature_1},{temperature_2}"
        
        return "65535,32768,1023,512" # just for testing
    
    def get_grating_angle(self):
        return self.motor.get_grating_angle()

    def start_collection(self):
        # TODO: this loop should start data collection. 
        self.motor.enable_motor(True)
            # Open (or create) a file to store the data
        with open('sensor_data1.txt', 'w') as file:
            for loop_number in range(1, 4):  # Outer loop, runs three times
                #TODO: calibration needs to be here
                for step_count in range(4000):  # Inner loop, runs 4000 times for each outer loop
                    # Get combined sensor reading
                    combined_data = self.combine_sensor_readings()

                    # Append the loop number to the data
                    data_to_write = f"{loop_number},{combined_data}\n"

                    # Write the data to the file
                    file.write(data_to_write)

                    # TODO: the motor needs to move one step after we collected the data
                    self.motor.move() # perform one step in the direction we need
                    # TODO: this should be in a try/catch block to catch any errors in the move.
                    
                # Optional: a small delay between each outer loop iteration
                #time.sleep(0.001)
                # TODO: call the calibration algorithm HERE
        self.motor.enable_motor(False)    
        print("One full sample complete for all LEDs. Data stored in 'sensor_data.txt'.")

# FOR TESTING ONLY. THIS CLASS SHOULD NOT HAVE A MAIN LOOP EVENTUALLY. 
def main():
    print("The payload control software has been started")
    payload_control = DataCollection()
    payload_control.start_collection()
    
    #grating_angle = payload_control.get_grating_angle()
    #print("The current motor angle is: {:.4f}".format(grating_angle))
    # testing if moving the motor updates the encoder value
    #payload_control.motor.move()
    #new_grating_angle = payload_control.get_grating_angle()
    #print("The current motor angle is: {:.4f}".format(new_grating_angle))


# Call the main function
if __name__ == "__main__":
    main()