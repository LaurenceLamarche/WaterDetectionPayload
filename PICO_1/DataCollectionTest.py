from machine import Pin, UART, I2C, ADC, RTC
import time
from time import sleep, time_ns
import uos

class DataCollectionTest:

    def __init__(self):
        
        # UART pico communication
        self.uart_id = 0
        self.baud_rate = 115200
        self.com1 = UART(self.uart_id, self.baud_rate)
        
        self.adc = ADC(26)  # Create an ADC object on GPIO 26
        
        #ADS1115 I2C connection
#         self.ADS = I2C(1, freq=400000, scl=Pin(11), sda=Pin(10)) # PICO 1 12C PINS
#         self.address = 72
        
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
    
    def readValueTest(self):
        value = self.adc.read_u16()
        print(value)
        return value
    
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

        
    def get_photodetector_value(self):
        #self.write(self.com1, 'photodetector')
        response = self.read(self.com1)
        if isinstance(response, str):
            return response  # String response
        else:
            print("Received raw data:", response)
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
                    value = self.readValueTest()
                    volts_data = (value / 65535) * 3.3
                    print("value = ", value, "\tVolts = ", volts_data) # TEST WITH PICO ADC (LAURENCE)
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

# FOR TESTING ONLY. THIS CLASS SHOULD NOT HAVE A MAIN LOOP EVENTUALLY. 
#def main():
#    print("The payload control software has been started")
#	 payload_control = DataCollection()
#	 payload_control.start_collection()

# Call the main function
#if __name__ == "__main__":
#    main()
