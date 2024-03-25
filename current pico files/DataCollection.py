from machine import Pin, UART, I2C, RTC, ADC
import time
from time import sleep, time_ns
import uos
from Motor import Motor
from PID import PID
from LED import LED
# march 14

class DataCollection:

    def __init__(self, com):
        # Initialize Motor instance
        self.motor = Motor()
        self.direction = False #counterclockwise TODO: FIGURE THIS OUT
        #self.direction = True #clockwise
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
        except Exception as e:
            #print("error reading value from ADC")
            #don't raise this error further to not interrupt sweep more than necessary
            rtc = RTC()
            current_time = rtc.datetime()
            timestamp = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(*current_time)
            err_msg = f"Failed to read ADC value, {e}, {timestamp}\n"
            with open('err_log.txt', 'a') as file:
                file.write(err_msg)
            return -1
    
    # UART STUFF

    def write(self, com1, message:str):
        #print(f'sending message: {message}')
        #message = message + '\n'
        try:
            com1.write(bytes(message,'utf-8'))
        except Exception as e:
            rtc = RTC()
            current_time = rtc.datetime()
            timestamp = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(*current_time)
            err_msg = f"Failed to send UART message, {e}, {timestamp}\n"
            raise Exception(err_msg) 


    def read(self, com1):
        try:
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
        except Exception as e:
            rtc = RTC()
            current_time = rtc.datetime()
            timestamp = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(*current_time)
            err_msg = f"Failed to send UART message, {e}, {timestamp}\n"
            raise Exception(err_msg)
        
    
    #only for test, in final version the motor will not need to change direction       
    def change_direction(self):
        if (self.direction): #reverse the direction
            self.motor.set_direction(False)
            self.direction = False
        else:
            self.motor.set_direction(True) #change motor's direction
            self.direction = True
        print("direction changed to ", self.direction)
        
        
    def temp_control(self):
        while True:
            self.temp_c = "0"
            while self.led_on:
                try:
                    pid = PID(1, 1, 0.2, setpoint=2.0)
        
                    pid.output_limits = (-1, 0)
                    output = pid(self.temp_volts)
                    self.led.pwm_pin.duty_u16(int(65535*abs(output)))
                    print("temp control: V: " + str(self.temp_volts) + " C: " + str(output))
             #       self.temp_v = str(volts_data)
                    self.temp_c = str(output)
                    time.sleep(5)
                except Exception as e:
                    rtc = RTC()
                    current_time = rtc.datetime()
                    timestamp = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(*current_time)
                    err_msg = f"error in TEC PWM control or PID control, {e}, {timestamp}\n"
                    with open('err_log.csv', 'a') as file:
                        file.write(err_msg)
            pass
        
    def send_err_log(self):
        try:
            with open('err_log.csv', mode='r') as file:
                line = file.readline()
                while line:
                    self.write(self.com1, line)  # Strip whitespace and newline characters
                    line = file.readline()
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except IOError as e:
            print(f"Error reading file {filename}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
    def start_collection(self):
        
        try:
            # SET FILENAME FOR PICO BACKUP
            rtc = RTC()
            current_time = rtc.datetime()
            # Format the current date and time as a timestamp string
            timestamp = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(*current_time)
            filename = "data_backup_" + timestamp + ".csv"
            
            # ENABLE THE MOTOR, Set initial direction to clockwise
            self.motor.enable_motor(True)
            self.motor.set_direction(self.direction)#True is CW, False is CCW
            
            # OPEN (OR CREATE) THE BACKUP FILE
            maximum = 0
            average = 0
            with open(filename, 'w') as file:
                for led_number in range(1, 5):  # Outer loop, (1, 5) runs three times (once per LED)
                    self.led = LED(led_number)
                    self.led_on = True
                    spectrum_started = False
                    base_voltage = 1.3
                    
                    #for step_count in range(6227):  # Inner loop, runs 4000 times for each outer loop
                    for step_count in range(2500):    
                            
                        # COLLECT PHOTODETECTOR DATA
                        value = self.readValue(3)
                        volts_data = value*(6.124*2)/(0xffff)
                        # Print data every 100 steps
                        average = average + volts_data # add to the running total
                        temp = self.readValue(self.led.adc_addr)
                        #temp = self.readValue(1)
                        #self.temp_volts = temp*(4.096*2)/(0xffff)
                        self.temp_volts = temp*(6.124*2)/(0xffff)
                        # new
                        if volts_data > base_voltage and not spectrum_started:
                            spectrum_started = True
                            print("spectrum_started")
                        elif volts_data < base_voltage and spectrum_started:
                            spectrum_started = False
                            self.led.pwm_pin.duty_u16(0)
                            print("nextled")
                            print("spectrum_stopped")
                            break
                        # END new
                        
                        if volts_data > maximum:
                            maximum = volts_data
                        if step_count % 100 == 0:
                            print(led_number, volts_data, base_voltage, spectrum_started, self.temp_volts, self.temp_c, self.led.adc_addr)
                            adc_value = self.temp_sensor.read_u16()
                            #adc_voltage = adc_value * 3.3 / 65535
                            
                            average = average/100
                            maximum = 0
                            average = 0
                            
                            # CHECK FOR STOP COMMAND FROM GROUND
                            ground_command = self.read(self.com1)
                            if ground_command is not None:
                                print(ground_command)
                                if ground_command == "STOP":
                                    return led_number, step_count
                                elif ground_command == "REVERSE":
                                    self.change_direction()
    
                        data_to_write = f"{led_number}, {step_count}, {volts_data}, {self.temp_volts}, {self.temp_c}\n"
                        file.write(data_to_write)
                        
                        # SEND DATA TO GROUND VIA UART COMS
                        self.write(self.com1, data_to_write)
                        
                        # MOVE MOTOR ONE STEP
                        self.motor.move() # perform one step in the direction we need
                        
                    # Optional: a small delay between each outer loop iteration
                    #time.sleep(0.1)
                    self.write(self.com1, "0, 0, 0\n") # Send confirmation when done with one LED
                    
                    ## JUST FOR TESTING WITH ONE LED
                    #self.change_direction()
                    #self.motor.set_direction(False)#True is CW, False is CCW
                
                # Turning off the LED
                self.led.pwm_pin.duty_u16(0)    
                self.led_on = False
                
                
                self.send_err_log()
                
                
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
                        try:
                            with open('err_log.csv', mode='w') as file:
                                pass
                        except Exception as e:
                            print("couldn't clear err_log.")
                        print("File deleted.")
                        break  # Exit the loop
            self.motor.enable_motor(False) 
            print("One full sample complete for all LEDs")
            return led_number, step_count
        
        
        except Exception as e:
            with open('err_log.csv', 'a') as file:
                #file.write(e)
                error_msg = str(e)
                file.write(error_msg)
            return led_number, step_count
        
        except KeyboardInterrupt:
            # If data collection is interrupted midway, we have to know where we are
            # Get the loop number and the number of steps completed
            data_to_send = f"{led_number}, {step_count}, {volts_data}, STOPPED\n"
            self.write(self.com1, data_to_send)
            return led_number, step_count

