from machine import ADC, Pin
import time

# Initialize ADC for thermistors (e.g., GP28 is ADC2, GP29 is ADC3)
thermistor_1 = ADC(28)

# Function to read and calculate the temperature from a thermistor
def read_temperature_from_thermistor(adc):
    # Constants for the thermistor and ADC
    R0 = 10000  # Resistance of the thermistor at 25 degrees Celsius (10k Ohms)
    T0 = 298.15  # Reference temperature (25°C in Kelvin)
    B = 3435  # The Beta value (from the datasheet)
    R_series = 10000  # The value of the series resistor (10k Ohms)
    ADC_max = 4095  # The maximum value of the ADC (12-bit ADC)
    
    ADC_value = adc.read_u16() >> 4  # Read the ADC value and convert it to 12-bit
    if ADC_value == 0:
        ADC_value = 1  # Prevent division by zero

    # Calculate the thermistor resistance
    R = R_series * ((65535 / ADC_value) - 1)

    # Calculate the temperature in Kelvin using the B-value equation
    T_inv = (1/T0) + (1/B) * math.log(R/R0)
    T_kelvin = 1 / T_inv

    # Convert the temperature to Celsius
    T_celsius = T_kelvin - 273.15

    return T_celsius


# Function to combine sensor readings into a single data packet
def combine_sensor_readings():
    # Read sensor values
    temperature_1 = read_temperature_from_thermistor(thermistor_1)
    temperature_2 = read_temperature_from_thermistor(thermistor_2)
    photodetector_value = read_photodetector()
    motor_angle = read_motor_angle()

    # Combine sensor readings
    # Assuming temperatures can fit in 12 bits, photodetector in 16 bits, and motor angle in 16 bits 
    # Now using 64-bit integer to fit 56 bits of data
    combined_data = (photodetector_value << 40) | (motor_angle << 24) | (temperature_1 << 12) | temperature_2
    
    # This is now using a 64-bit integer to fit 56 bits of data -- TODO: ensure this type wont get converted on other systems
    return combined_data


# Just testing, for now
while True:
    #just testing, we don't need these if we have the combine_sensor_readings function working
    temp1 = read_temperature_from_thermistor(thermistor_1)
    print(f"Temperature 1: {temp1} C")
    
    time.sleep(2)  # Sleep for 3 seconds before reading again
    
    combined_data = combine_sensor_readings()
    print(f"Combined data: {combined_data}")
    
