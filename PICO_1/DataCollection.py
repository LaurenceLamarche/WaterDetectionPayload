from machine import Pin, UART
import time
from time import sleep, time_ns
import uos
from Motor import Motor

class DataCollection:

    def __init__(self):
        # Initialize Motor instance
        self.motor = Motor()
        
        # UART pico communication
        self.uart_id = 0
        self.baud_rate = 115200
        self.com1 = UART(self.uart_id, self.baud_rate)

    def write(self, com1, message:str):
        print(f'sending message: {message}')
        message = message + '\n'
        com1.write(bytes(message,'utf-8'))

    def read(self, com1):
        timeout = 1000000000 # 1 second
        start_time = time_ns()
        current_time = start_time
        message_end = False
        message = ""
        while (not message_end) and (current_time <= (start_time + timeout)):
            current_time = time_ns()
            if (com1.any() > 0):
                #print(com1.read())
                message = message + com1.read().decode('utf-8')
                if '\n' in message:
                    message_end = True
                    message = message.strip('\n')
                    # print(f'received message: {message}')
                    return message
        else:
            return None
        
#     def read(self, com1):
#         timeout = 1000000000  # 1 second
#         start_time = time_ns()  # Use time.ticks_us for better precision
#         message_end = False
#         raw_message = b''
#         while not message_end and time.ticks_diff(time_ns(), start_time) < timeout:
#             if com1.any() > 0:
#                 byte = com1.read(1)
#                 raw_message += byte
#                 if byte == b'\n':
#                     message_end = True
# 
#         try:
#             message = raw_message.decode('utf-8').strip()
#             return message
#         except:
#             print("Received non-UTF-8 data")
#             return raw_message  # or handle differently

    # Function to combine sensor readings into a single data packet
    def combine_sensor_readings(self):
        print(time_ns)
        # Read sensor values
        # TODO: replace with actual real functions from DataCollectionTest.py
        #photodetector_value = self.get_photodetector_value()
        photodetector_value = "1"
        #motor_angle = self.get_grating_angle()
        motor_angle = "1.0"
        temperature_1 = "1023"
        temperature_2 = "512"
        combined_data = f"{photodetector_value},{motor_angle},{temperature_1},{temperature_2}"
        
        #return "65535,32768,1023,512" # just for testing
        print(time_ns)
        return combined_data
    
    
    def get_grating_angle(self):
        return self.motor.get_grating_angle()
    
#     def get_photodetector_value(self):
#         self.write(self.com1, f'photodetector')
#         #TODO: put in try catch
#         #return self.read(self.com1) # will this work ?
        
    def get_photodetector_value(self):
        #self.write(self.com1, 'photodetector')
        response = self.read(self.com1)
        if isinstance(response, str):
            return response  # String response
        else:
            print("Received raw data:", response)
            # Handle raw data response here, if necessary

    def start_collection(self):
        self.motor.enable_motor(True)
        self.motor.set_direction(False)#True is CW, False is CCW 
            # Open (or create) a file to store the data
        with open('photodetector.txt', 'w') as file:
            for loop_number in range(1, 2):  # Outer loop, runs three times
                #TODO: calibration needs to be here
                for step_count in range(5000):  # Inner loop, runs 4000 times for each outer loop
                    # Get combined sensor reading
                    #print("before: "+str(time_ns()))
                    #combined_data = self.combine_sensor_readings()
                    #print(combined_data)
                    #Append the loop number to the data
                    #data_to_write = f"{loop_number},{combined_data}\n"

                    # Write the data to the file
                    #file.write(data_to_write)
                    #time.sleep(0.1)
                    #print("after: "+str(time_ns()))
                    # Move one step after data is collected
                    self.motor.move() # perform one step in the direction we need
                    
                    #print("grating angle is:", self.motor.get_grating_angle())
                    # TODO: this should be in a try/catch block to catch any errors in the move.
                # Optional: a small delay between each outer loop iteration
                time.sleep(0.1)
                # TODO: call the calibration algorithm HERE
        self.motor.enable_motor(False)    
        print("One full sample complete for all LEDs. Data stored in 'sensor_data.txt'.")

# FOR TESTING ONLY. THIS CLASS SHOULD NOT HAVE A MAIN LOOP EVENTUALLY. 
#def main():
#    print("The payload control software has been started")
#    payload_control = DataCollection()
#    payload_control.start_collection()
    
    #grating_angle = payload_control.get_grating_angle()
    #print("The current motor angle is: {:.4f}".format(grating_angle))
    # testing if moving the motor updates the encoder value
    #payload_control.motor.move()
    #new_grating_angle = payload_control.get_grating_angle()
    #print("The current motor angle is: {:.4f}".format(new_grating_angle))


# Call the main function
#if __name__ == "__main__":
#    main()
