from machine import Pin, UART, I2C, RTC, ADC
import time
from time import sleep, time_ns
import uos
from Motor import Motor

class DataCollection:

    def __init__(self, com):
        # Initialize Motor instance
        self.motor = Motor()
        self.direction = False #counterclockwise
        self.stop = False
        
        # UART pico communication
        #self.uart_id = 0
        #self.baud_rate = 115200
        #self.com1 = UART(self.uart_id, self.baud_rate)
        self.com1 = com
        #ADS1115 I2C connection
        
        self.ADS = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2)) # PICO 12C PINS
        self.address = 72
        self.temp_sensor = ADC(26)
        
    # Functions to read from the ADC
    def readConfig(self):
        self.ADS.writeto(self.address, bytearray([1]))
        result = self.ADS.readfrom(self.address, 2)
        return result[0]<<8 | result[1]

    def readValue(self, channel):
        try:
            self.ADS.writeto(self.address, bytearray([0]))
            result = self.ADS.readfrom(self.address, 2)
            
            config = self.readConfig()
            config &= ~(7<<12) & ~(7<<9)
            config |= (7 & (4+channel))<<12
            #config |= (1<<9) #gain of 4.096 V
            config |= (1<<15)
            
            config = [ int(config>>i & 0xff) for i in (8,0)]
            self.ADS.writeto(self.address, bytearray([1] + config))
            
            config = self.readConfig()
            while (config & 0x8000) ==0:
                config = self.readConfig()
            #print(config)
            self.ADS.writeto(self.address, bytearray([0]))
            result = self.ADS.readfrom(self.address, 2)
            return result[0]<<8 | result[0]
        except:
            #print("error reading value from ADC")
            return -1
    
    # UART STUFF

    def write(self, com1, message:str):
        #print(f'sending message: {message}')
        #message = message + '\n'
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
        
    
    def get_grating_angle(self):
        return self.motor.get_grating_angle()
    
        
    def get_photodetector_value(self):
        #self.write(self.com1, 'photodetector')
        response = self.read(self.com1)
        if isinstance(response, str):
            return response  # String response
        #else:
            #print("Received raw data:", response)
            # Handle raw data response here, if necessary
            
    def change_direction(self):
        self.direction = not self.direction #reverse the direction
        self.motor.set_direction(self.direction) #change motor's direction
            
    def start_collection(self):
        
        try:
            # SET FILENAME FOR PICO BACKUP
            rtc = RTC()
            current_time = rtc.datetime()
            # Format the current date and time as a timestamp string
            timestamp = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(*current_time)
            filename = "data_backup_" + timestamp + ".csv"
            #filenmae = 'datasweep_Feb9_1050_watertrial.' # Use this to create a custom filename
            
            # ENABLE THE MOTOR, Set initial direction to clockwise
            #current_dir = self.direction
            self.motor.enable_motor(True)
            #self.motor.set_direction(True)#True is CW, False is CCW
            
            # OPEN (OR CREATE) THE BACKUP FILE
            maximum = 0
            average = 0
            with open(filename, 'w') as file:
                for led_number in range(1, 2):  # Outer loop, (1, 4) runs three times (once per LED)
                    
                    #for step_count in range(6227):  # Inner loop, runs 4000 times for each outer loop
                    for step_count in range(1000):    
                            
                        # COLLECT PHOTODETECTOR DATA
                        value = self.readValue(3)
                        volts_data = value*(6.124*2)/(0xffff)
                        # Print data every 100 steps
                        average = average + volts_data # add to the running total
                        
                        if volts_data > maximum:
                            maximum = volts_data
                        if step_count % 100 == 0:
                            adc_value = self.temp_sensor.read_u16()
                            adc_voltage = adc_value * 3.3 / 65535
                            
                            average = average/100
                            
                            value = self.readValue(2)
                            ts_1 = value*(6.124*2)/(0xffff)
                        
                            value = self.readValue(1)
                            ts_2 = value*(6.124*2)/(0xffff)
                        
                            value = self.readValue(0)
                            ts_3 = value*(6.124*2)/(0xffff)
                            
                            #print("Photodiode: ", maximum, "\tT_1 = ", ts_1, "\tT_2 = ", ts_2, "\tT_3 = ", ts_3, "\tT_PD = ", adc_voltage)
                            print("Photodiode: ", average, "\tT_1 = ", ts_1, "\tT_2 = ", ts_2, "\tT_3 = ", ts_3, "\tT_PD = ", adc_voltage)
                            
                            # print("ADC_value = ", value, "\tADC_volts = ", maximum, "\tphotodiode_temp_value = ", adc_value, "\tphotodiode_temp_volts = ", adc_voltage)
                            maximum = 0
                            average = 0
#                             grating_angle = self.get_grating_angle()
#                             print(f"step_count={step_count}, grating angle is: {grating_angle}\n")
                            
                            # CHECK FOR STOP COMMAND FROM GROUND
                            ground_command = self.read(self.com1)
                            if ground_command is not None:
                                print(ground_command)
                                if ground_command == "STOP":
                                    return led_number, step_count
                                elif ground_command == "REVERSE":
                                    self.change_direction()
#                             
                        data_to_write = f"{led_number}, {step_count}, {volts_data}\n"
                        file.write(data_to_write)
                        
                        # SEND DATA TO GROUND VIA UART COMS
                        self.write(self.com1, data_to_write)
                        
                        # MOVE MOTOR ONE STEP
                        #self.motor.move() # perform one step in the direction we need
                        
                    # Optional: a small delay between each outer loop iteration
                    time.sleep(0.1)
                    self.write(self.com1, "0, 0, 0\n") # Send confirmation when done with one LED
                    
                    ## JUST FOR TESTING WITH ONE LED
                    #self.motor.set_direction(False)#True is CW, False is CCW
                    
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
            return led_number, step_count
        
        except KeyboardInterrupt:
            # If data collection is interrupted midway, we have to know where we are
            # Get the loop number and the number of steps completed
            data_to_send = f"{led_number}, {step_count}, {volts_data}, STOPPED\n"
            self.write(self.com1, data_to_send)
            return led_number, step_count


