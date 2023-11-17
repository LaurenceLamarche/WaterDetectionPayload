import machine
import time

# Define the pins connected to the A4988 driver
step_pin = machine.Pin(3, machine.Pin.OUT)  # verify this
dir_pin = machine.Pin(2, machine.Pin.OUT)   # verify this
enable_pin = machine.Pin(14, machine.Pin.OUT)
MS1_pin = machine.Pin(7, machine.Pin.OUT)
MS2_pin = machine.Pin(6, machine.Pin.OUT)
MS3_pin = machine.Pin(5, machine.Pin.OUT)

# Enable the motor (set enable pin high)
enable_pin.value(1)

# Set step size, MS3 we dont care about
MS1_pin.value(0)
MS2_pin.value(0)

# Set the direction (0 for one direction, 1 for the other)
dir_pin.value(1)  # Change to 1 if you want to reverse the direction

# Define the number of steps for a full revolution (may vary with your motor)
steps_per_rev = 20000

# Define the number of steps for half a revolution (180 degrees)
num_steps = int(steps_per_rev / 2)

# Calculate the delay for a 2-second half revolution
total_time = 120  # total time for half revolution in seconds
delay = total_time / num_steps  # delay between steps

# Function to perform a specified number of steps
def perform_steps(num_steps, delay):
    print("Performing steps...")
    for _ in range(num_steps):
        step_pin.on()
        time.sleep(delay / 2)  # Half the delay for the step on time
        step_pin.off()
        time.sleep(delay / 2)  # Half the delay for the step off time

# Rotate the motor by 180 degrees (half a revolution)
perform_steps(num_steps, delay)

# Ensure that the stepper motor is stopped when done
step_pin.off()

# Disable the motor (set enable pin low) to save power when not in use
enable_pin.value(0)
