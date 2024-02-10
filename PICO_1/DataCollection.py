from machine import Pin, UART, I2C, RTC
import time
from time import sleep, time_ns
import uos
from Motor import Motor
from ir_rx.print_error import print_error
from ir_rx.nec import NEC_8

class DataCollection:

    def __init__(self):
        # Initialize Motor instance
        self.motor = Motor()
        self.direction = False
        self.stop = False
        
        # UART pico communication
        self.uart_id = 0
        self.baud_rate = 115200
        self.com1 = UART(self.uart_id, self.baud_rate)
        #ADS1115 I2C connection
        
        self.ADS = I2C(1, freq=400000, scl=Pin(11), sda=Pin(10)) # PICO 1 12C PINS
        self.address = 72
        
    '''
    def decodeKeyValue(data):
        return data
    def callback(data, addr, ctrl):
        Stop = 28
        start = 24
        change_dir = 82
        #global measure
        if data < 0:  # NEC protocol sends repeat codes.
            pass
        else:
            print(data)
            if data == Start:
                print('start')
                #measure = True
                #com1.write('photodetector')
                
            elif data == Stop:
                self.stop = True
                print('stop')
                
            elif data == change_dir:
                print(self.direction)
                self.direction = not self.direction
                
                '''
    # Functions to read from the ADC
    def readConfig(self):
        self.ADS.writeto(self.address, bytearray([1]))
        result = self.ADS.readfrom(self.address, 2)
        return result[0]<<8 | result[1]

    def readValue(self, channel):
        self.ADS.writeto(self.address, bytearray([0]))
        result = self.ADS.readfrom(self.address, 2)
        
        config = self.readConfig()
        config &= ~(7<<12) & ~(7<<9)
        config |= (7 & (4+channel))<<12
        config |= (1<<9) #gain of 4.096 V
        config |= (1<<15)
        
        config = [ int(config>>i & 0xff) for i in (8,0)]
        self.ADS.writeto(self.address, bytearray([1] + config))
        
        config = self.readConfig()
        while (config & 0x8000) ==0:
            config = self.readConfig()
        
        self.ADS.writeto(self.address, bytearray([0]))
        result = self.ADS.readfrom(self.address, 2)
        return result[0]<<8 | result[0]
    
    # UART STUFF

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

    # TEST Function to combine sensor readings into a single data packet
    def combine_sensor_readings(self):
        #print(time_ns)
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
        #print(time_ns)
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
        #else:
            #print("Received raw data:", response)
            # Handle raw data response here, if necessary
            
    def start_collection_test(self):
        # Open (or create) a file to store the data
        rtc = RTC()
        current_time = rtc.datetime()
        # Format the current date and time as a timestamp string
        timestamp = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(*current_time)
        filename = "outgoing_data_" + timestamp + ".txt"
        
        with open(filename, 'w') as file:
            for led_number in range(1, 4):  # Outer loop, (1, 4) runs three times (once per LED)
                for step_count in range(100):  # Inner loop, runs 4000 times for each outer loop
                    
                    value = self.readValue(0)
                    #volts_data = value*(4.096*2)/(0xffff)
                    volts_data = (value / 65535) * 3.3
                    print("value = ", value, "\tVolts = ", volts_data) 
                    data_to_write = f"{led_number}, {step_count}, {volts_data}\n"
                    file.write(data_to_write)
                    
                    # UART COMS
                    self.write(self.com1, data_to_write)
                # Optional: a small delay between each outer loop iteration
                time.sleep(0.1)
                self.write(self.com1, "0, 0, 0") # Send confirmation when done with one LED
            
            # Wait for confirmation message
            confirmation_received = False
            print("Data sent for 3 LEDs, waiting for reception confirmation")
            while not confirmation_received:
                confirmation_message = self.read(self.com1)
                print("received some confirmation message: ")
                print(confirmation_message)
                if confirmation_message == "DATA RECEIVED": #TODO: change this
                    confirmation_received = True
                    uos.remove(filename)  # Delete the file
                    print("File deleted.")
                    break  # Exit the loop
        print("One full sample complete for all LEDs")

    def start_collection(self):
        #pin_ir = Pin(14, Pin.IN)
        #ir = NEC_8(pin_ir, self.callback)  # Instantiate receiver
        #ir.error_function(print_error)  # Show debug information
        current_dir = self.direction
        self.motor.enable_motor(True)
        self.motor.set_direction(True)#True is CW, False is CCW
        #self.motor.set_direction(self.direction)#
            # Open (or create) a file to store the data
        with open('datasweep_Feb9_1050_trial1.csv', 'w') as file:
            for loop_number in range(1, 2):  # Outer loop, runs three times
                #TODO: calibration needs to be here
                for step_count in range(10000):  # Inner loop, runs 4000 times for each outer loop
                    # Get combined sensor reading
                    #print("before: "+str(time_ns()))
                    #combined_data = self.combine_sensor_readings()
                    #print(combined_data)
                    #Append the loop number to the data
                    #data_to_write = f"{loop_number},{combined_data}\n"

                    # Write the data to the file
                    
                    if current_dir != self.direction:
                        self.motor.set_direction(self.direction)
                        current_dir = self.direction
                    
                    #time.sleep(0.1)
                    #print("after: "+str(time_ns()))
                    # Move one step after data is collected
                    self.motor.move() # perform one step in the direction we need
                    value = self.readValue(0)
                    #print("value = ", value, "\tVolts = ",value*(4.096*2)/(0xffff)) # TEST 2 (LAURENCE)
                    volts_data = value*(4.096*2)/(0xffff)
                    #data_to_write = f"{loop_number},{volts_data}\n"
                    data_to_write = f"{step_count}, {volts_data}\n"
                    file.write(data_to_write)
                    #print("grating angle is:", self.motor.get_grating_angle())
                    # TODO: this should be in a try/catch block to catch any errors in the move.
                    if step_count % 100 ==0:
                        print(str(self.stop) + ' ' + str(step_count %100))
                    if self.stop == True:
                        self.stop = False
                        break
                # Optional: a small delay between each outer loop iteration
                time.sleep(0.1)
                # TODO: call the calibration algorithm HERE
        self.motor.enable_motor(False)    
        #print("One full sample complete for all LEDs. Data stored in 'sensor_data.txt'.")

# FOR TESTING ONLY. THIS CLASS SHOULD NOT HAVE A MAIN LOOP EVENTUALLY. 
#def main():
#    print("The payload control software has been started")
# payload_control = DataCollection()
# payload_control.start_collection()
    
    #grating_angle = payload_control.get_grating_angle()
    #print("The current motor angle is: {:.4f}".format(grating_angle))
    # testing if moving the motor updates the encoder value
    #payload_control.motor.move()
    #new_grating_angle = payload_control.get_grating_angle()
    #print("The current motor angle is: {:.4f}".format(new_grating_angle))


# Call the main function
#if __name__ == "__main__":
#    main()
