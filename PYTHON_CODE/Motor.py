import machine
import time

class Encoder:
    def __init__(self, clk_pin, dt_pin, cpr):
        self.clk_pin = machine.Pin(clk_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.dt_pin = machine.Pin(dt_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.counter = 0
        self.clk_last_state = self.clk_pin.value()
        self.cpr = cpr

    def update(self):
        clk_state = self.clk_pin.value()
        dt_state = self.dt_pin.value()

        if clk_state != self.clk_last_state:
            if dt_state != clk_state:
                self.counter += 1
            else:
                self.counter -= 1
            self.clk_last_state = clk_state
        return self.counter

    def get_count(self):
        return self.counter

    def reset(self):
        self.counter = 0
    
    def get_angle(self):
        # Calculate the angle
        print("getting grating angle from the Encoder...")
        print("current count is: ", self.get_count())
        return (self.get_count() / self.cpr) * 360


class Motor:
    def __init__(self):
        # Define the pins connected to the A4988 driver
        self.step_pin = machine.Pin(3, machine.Pin.OUT)
        self.dir_pin = machine.Pin(2, machine.Pin.OUT)
        self.enable_pin = machine.Pin(4, machine.Pin.OUT)
        self.MS1_pin = machine.Pin(7, machine.Pin.OUT)
        self.MS2_pin = machine.Pin(6, machine.Pin.OUT)
        self.MS3_pin = machine.Pin(5, machine.Pin.OUT)

        #TODO: Verify these are the right pins
        # Initialize Encoder
        self.encoder = Encoder(clk_pin=24, dt_pin=25, cpr=300)  

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

    #TODO: test this
    def get_grating_angle(self):
        print("getting grating angle from the Motor...")
        return self.encoder.get_angle()

    def move_half_turn(self, num_steps, total_time):
        # Calculate the delay based on the total time and the number of steps
        delay = total_time / num_steps
        self.enable_motor(True) # We don't know what state the motor is going to be in

        print("Performing move...")
        for _ in range(num_steps):
            self.step_pin.on()
            time.sleep(delay / 2)  # Half the delay for the step on time
            print("moving")
            self.step_pin.off()
            time.sleep(delay / 2)  # Half the delay for the step off time
            self.encoder.update()
        # Ensure that the stepper motor is stopped when done
        self.step_pin.off()
        self.enable_motor(False)

    def move(self):
        # we use the fixed delay
        print("Performing move...")
        self.step_pin.on()
        time.sleep(self.delay)  # ensure it doesn't move so fast
        self.step_pin.off()
        time.sleep(self.delay)  
        self.encoder.update()
        #TODO: return true if move was successful. So, motor has to be aware of its position? Does it?

#Use this for testing
while True:
    motor = Motor()
    motor.move_half_turn(10000, 120) #half a full turn is 10000 steps, 120seconds is 2 minutes.
