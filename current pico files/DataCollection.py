from machine import Pin, UART, I2C, PWM, RTC
import time
import uos
from Motor import Motor
from PID import PID
from LED import LED



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
        
        self.ADS = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2)) # PICO 1 12C PINS
        self.address = 72
        self.temp_sensor = ADC(26)
        
        self.led_on = False
        self.temp_volts = 0
        self.temp_c = ''
        self.led = None
        
    # Functions to read from the ADC
    def readConfig(self):
        self.ADS.writeto(self.address, bytearray([1]))
        result = self.ADS.readfrom(self.address, 2)
        return result[0]<<8 | result[1]

    def readValue(self, channel):
        self.ADS.writeto(self.address, bytearray([0]))
        result = self.ADS.readfrom(self.address, 2)
        
        config = self.readConfig()
        config &= ~(7<<12) & ~(7<<9) #doing this sets a default gain of 6.124 volts
        config |= (7 & (4+channel))<<12
        #config |= (1<<9) #gain of 4.096 V
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
        start_time = time.time_ns()
        current_time = start_time
        message_end = False
        message = ""
        while (not message_end) and (current_time <= (start_time + timeout)):
            current_time = time.time_ns()
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
        
'''
    # TEST Function to combine sensor readings into a single data packet
    def combine_sensor_readings(self):
        print(time.time_ns)
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
        print(time.time_ns)
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
            # Handle raw data response here, if necessary'''
    def temp_control(self):
        while True:
            self.temp_c = "0"
            while self.led_on:
                pid = PID(1, 1, 0.2, setpoint=2.0)

                pid.output_limits = (-1, 0)
                output = pid(self.temp_volts)
                self.led.pwm_pin.duty_u16(int(65535*abs(output)))
                print("temp control: V: " + str(self.temp_volts) + " C: " + str(output))
         #       self.temp_v = str(volts_data)
                self.temp_c = str(output)
                time.sleep(5)
            pass
        
    def start_collection(self):
        # SET FILENAME FOR PICO BACKUP
        try:
            rtc = RTC()
            current_time = rtc.datetime()
            # Format the current date and time as a timestamp string
            timestamp = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(*current_time)
            filename = "1550_model_data_" + timestamp + ".csv"
            #filename = 'datasweep_Feb23.csv' # Use this to create a custom filename
            print(filename)
            # ENABLE THE MOTOR, Set initial direction to clockwise
            current_dir = self.direction
            self.motor.enable_motor(True)
            self.motor.set_direction(True)#True is CW, False is CCW
            ##
            # OPEN (OR CREATE) THE BACKUP FILE
            #try:
            maximum = 0
            with open(filename, 'w') as file:
                
                for led_number in range(1, 5):  # Outer loop, (1, 4) runs three times (once per LED)
                    #self.ADS = I2C(1, freq=400000, scl=Pin(11), sda=Pin(10))
                    self.led = LED(led_number)
                    self.led_on = True
                    spectrum_started = False
                    base_voltage = 0.5
                    for step_count in range(6227):  # Inner loop, runs 4000 times for each outer loop
                           
                        # CHECK TO SEE IF DIRECTION CHANGED
                        if current_dir != self.direction:
                            self.motor.set_direction(self.direction)
                            current_dir = self.direction
                            
                        # COLLECT PHOTODETECTOR DATA
                        value = self.readValue(3)
                        
                        #print(value)
                        #volts_data = value*(4.096*2)/(0xffff)
                        volts_data = value*(6.124*2)/(0xffff)
                        if volts_data > base_voltage and not spectrum_started:
                            spectrum_started = True
                            print("spectrum_started")
                        elif volts_data < base_voltage and spectrum_started:
                            spectrum_started = False
                            self.led.pwm_pin.duty_u16(0)
                            print("nextled")
                            print("spectrum_stopped")
                            break
                        
                        if volts_data > maximum:
                            maximum = volts_data
                        #collect temperature Data
                        temp = self.readValue(self.led.adc_addr)
                        #temp = self.readValue(1)
                        #self.temp_volts = temp*(4.096*2)/(0xffff)
                        self.temp_volts = temp*(6.124*2)/(0xffff)
                        #print(self.temp_volts)
                        # Print data every 100 steps
                        if step_count % 100 == 0:
                            print("Photodiode: ", maximum, "\tT_PD = ", adc_voltage, "\tT_led = ", temp_volts)
                            maximum = 0
                            
                            
                        data_to_write = f"{led_number}, {step_count}, {volts_data}, {self.temp_volts}, {self.temp_c}\n"
                        file.write(data_to_write)
                        
                        # UART COMS
                        self.write(self.com1, data_to_write)
                        
                        # MOVE MOTOR ONE STEP
                        self.motor.move() # perform one step in the direction we need
                        #grating_angle = self.get_grating_angle()
                        #print(f"step_count={step_count}, grating angle is: {grating_angle}\n")
                        # CHECK FOR STOP COMMAND
                        if self.stop == True:
                            self.stop = False
                            break
                    # Optional: a small delay between each outer loop iteration
                    time.sleep(0.1)
                    self.write(self.com1, "0, 0, 0\n") # Send confirmation when done with one LED
                    
                    ## JUST FOR TESTING WITH ONE LED
                    #self.motor.set_direction(False)#True is CW, False is CCW
                    
                self.led_on = False
                
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
            
            self.motor.enable_motor(False) 
            print("One full sample complete for all LEDs")
            
        except KeyboardInterrupt:
            # If data collection is interrupted midway, we have to know where we are
            # Get the loop number and the number of steps completed
            data_to_send = f"{led_number}, {step_count}, {volts_data}, STOPPED\n"
            self.write(self.com1, data_to_send)
            return led_number, step_count
        
    







