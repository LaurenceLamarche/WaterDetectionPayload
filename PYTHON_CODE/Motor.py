import machine
import time

class Motor:
    def __init__(self):
        # Define the pins connected to the A4988 driver
        self.step_pin = machine.Pin(3, machine.Pin.OUT)
        self.dir_pin = machine.Pin(2, machine.Pin.OUT)
        self.enable_pin = machine.Pin(14, machine.Pin.OUT)
        self.MS1_pin = machine.Pin(7, machine.Pin.OUT)
        self.MS2_pin = machine.Pin(6, machine.Pin.OUT)
        self.MS3_pin = machine.Pin(5, machine.Pin.OUT)

        # Set initial motor state
        self.enable_motor(False)
        self.set_step_size(False, False)
        self.set_direction(True)
        self.delay = 0.0001 # Verify that this is ok

        # Define the number of steps for a full revolution (may vary with your motor)
        self.steps_per_rev = 20000

        # Calculate the delay for a 2-second half revolution
        self.total_time = 120  # Total time for half revolution in seconds

    def enable_motor(self, enable):
        # Enable or disable the motor
        self.enable_pin.value(enable)

    def set_step_size(self, MS1, MS2):
        # Set step size
        self.MS1_pin.value(MS1)
        self.MS2_pin.value(MS2)

    def set_direction(self, direction):
        # Set the direction
        self.dir_pin.value(direction)

    def move_half_turn(self, num_steps, total_time):
        # Calculate the delay based on the total time and the number of steps
        delay = total_time / num_steps
        self.enable_motor(True) # We don't know what state the motor is going to be in

        print("Performing move...")
        for _ in range(num_steps):
            self.step_pin.on()
            time.sleep(delay / 2)  # Half the delay for the step on time
            self.step_pin.off()
            time.sleep(delay / 2)  # Half the delay for the step off time

        # Ensure that the stepper motor is stopped when done
        self.step_pin.off()
        self.enable_motor(False)

    def move(self):
        # we now want the delay to be fixed 

        print("Performing move...")
        self.step_pin.on()
        time.sleep(self.delay)  # Half the delay for the step on time
        self.step_pin.off()
        time.sleep(self.delay)  # Half the delay for the step off time

        # Ensure that the stepper motor is stopped when done
        self.step_pin.off()
        self.enable_motor(False)
