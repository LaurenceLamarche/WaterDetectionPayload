from machine import ADC, Pin
import time
import math

# Initialize ADC for thermistors (e.g., GP28 is ADC2, GP29 is ADC3)
thermistor_1 = ADC(28)
thermistor_2 = ADC(29)
# Using a potentiometer or similar analog sensor for the angle, I would use an ADC like this:
motor_angle_adc = ADC(26)  # Assuming the angle sensor is connected to GP26
# Initialize ADC for the photodetector (e.g., GP27 is ADC1)
photodetector_adc = ADC(27)

# Define the pins connected to the A4988 driver
step_pin = machine.Pin(2, machine.Pin.OUT)  # Replace 2 with actual GPIO pin
dir_pin = machine.Pin(4, machine.Pin.OUT)   # Replace 4 with actual GPIO pin

# Set the direction (0 for one direction, 1 for the other)
dir_pin.value(0)  # Change to 1 if you want to reverse the direction

# Define the number of steps for a full revolution (verify this)
steps_per_rev = 20000

# Define the delay between steps (adjust for desired speed)
delay = 0.01  # Adjust for your motor and application


# Function to perform a specified number of steps
def perform_steps(num_steps):
    for _ in range(num_steps):
        step_pin.on()
        time.sleep_us(2)  # Adjust if needed
        step_pin.off()
        time.sleep_us(2)  # Adjust if needed

  
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

# Function to read the motor angle value

def read_motor_angle():
    # Read the ADC value
    # value = motor_angle_adc.read_u16() >> 4  # Converts to 12-bit
    # TODO: this should be read from encoder.
    value = motor_angle_adc.read_u16()
    
    # Convert the ADC value to an angle here. TODO: VERIFY THIS
    # If the potentiometer gives 0 to 3.3V over 0 to 270 degrees:
    # angle = (value / 4095.0) * 270.0  # Scale the 12-bit ADC value to degrees
    angle = (value / 65535.0) * 270.0  # Scale the 16-bit ADC value to degrees
    return angle

# Function to read the photodetector value
def read_photodetector():
    # Read the 16-bit value from the photodetector ADC
    # value = photodetector_adc.read_u16() >> 4  # Converts to 12-bit
    value = photodetector_adc.read_u16()
    
    # TODO: convert this to a meaningful measurement depending on photodetector's characteristics
    return value

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
    combined_data_string = f"{photodetector_value},{motor_angle},{temperature_1},{temperature_2}"
    
    # This is now using a 64-bit integer to fit 56 bits of data -- TODO: ensure this type wont get converted on other systems
    # We can choose which data we need
    return combined_data_string


# Just testing, for now
while True:
    #just testing, we don't need these if we have the combine_sensor_readings function working
    temp1 = read_temperature_from_thermistor(thermistor_1)
    temp2 = read_temperature_from_thermistor(thermistor_2)
    motor_angle = read_motor_angle()
    photodetector_value = read_photodetector()
    
    print(f"Temperature 1: {temp1} C")
    print(f"Temperature 2: {temp2} C")
    print(f"Motor Angle: {motor_angle} degrees")
    print(f"Photodetector Value: {photodetector_value}")
    time.sleep(2)  # Sleep for 3 seconds before reading again
    
    #if all the previous functions work, test that this has the predicted features.
    combined_data = combine_sensor_readings()
    print(f"Combined data: {combined_data}")
    
