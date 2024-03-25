#March 14

import machine
import time

class Encoder:
    def __init__(self, clk_pin, dt_pin, cpr):
        #self.clk_pin = machine.Pin(clk_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        #self.dt_pin = machine.Pin(dt_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.clk_pin = machine.Pin(clk_pin, machine.Pin.IN)
        self.dt_pin = machine.Pin(dt_pin, machine.Pin.IN)
        self.counter = 0
        self.clk_last_state = self.clk_pin.value()
        self.cpr = cpr

    def update(self):
        clk_state = self.clk_pin.value()
        dt_state = self.dt_pin.value()
#         print("entered udpate function")
#         print("clk_state = ", clk_state)
#         print("dt_state = ", dt_state)
#        print("clk_last_state = ", self.clk_last_state)
        #if clk_state != self.clk_last_state:
#            print("first check done")
        if dt_state != clk_state:
#                print("second check done")
            self.counter += 1
            #else:
                #self.counter -= 1
            self.clk_last_state = clk_state
        #print("grating angle is:", self.get_angle())
        #print("counter is: ", self.counter)
        return self.counter

    def get_count(self):
        return self.counter

    def reset(self):
        self.counter = 0
    
    def get_angle(self):
        # Calculate the angle
        return (self.get_count() / (self.cpr*(99+1044/2057))) * 360


class Motor:
    def __init__(self):
        # Define the pins connected to the A4988 driver
        self.step_pin = machine.Pin(16, machine.Pin.OUT)
        self.dir_pin = machine.Pin(15, machine.Pin.OUT)
        self.sleep_pin = machine.Pin(17, machine.Pin.OUT) # was never set before
        self.reset_pin = machine.Pin(9, machine.Pin.OUT) # was never set before
        self.enable_pin = machine.Pin(22, machine.Pin.OUT)
        self.MS1_pin = machine.Pin(21, machine.Pin.OUT)
        self.MS2_pin = machine.Pin(20, machine.Pin.OUT)
        self.MS3_pin = machine.Pin(19, machine.Pin.OUT)

        # Initialize Encoder
        self.encoder = Encoder(clk_pin=10, dt_pin=28, cpr=300)

        # Set initial motor state
        self.enable_motor(False)
        self.set_step_size(False, False, False)
        self.set_direction(True)
        self.delay = 0.012 # TODO: Optimize this

        # Define the number of steps for a full revolution (may vary with your motor)
        self.steps_per_rev = 20000

        # Calculate the delay for a 2-second half revolution
        self.total_time = 120  # Total time for half revolution in seconds

    def enable_motor(self, enable):
        # Enable or disable the motor
        self.enable_pin.value(not enable)
        # They should be set together to high
        self.sleep_pin.value(enable)
        self.reset_pin.value(enable)

    def set_step_size(self, MS1, MS2, MS3):
        # Set microstep values step size
        self.MS1_pin.value(MS1)
        self.MS2_pin.value(MS2)
        self.MS3_pin.value(MS3) # was never set before

    def set_direction(self, direction):
        # Set the direction
        self.dir_pin.value(direction)

    def get_grating_angle(self):
        return self.encoder.get_angle()
    
    # TODO: Maybe use this for calibration?
    def move_half_turn(self, num_steps, total_time):
        # Calculate the delay based on the total time and the number of steps
        delay = total_time / num_steps
        self.enable_motor(True) # We don't know what state the motor is going to be in

        print("Performing full move...")
        for _ in range(num_steps):
            self.step_pin.on()
            time.sleep(delay / 2)  # Half the delay for the step on time
            #print("moving")
            self.step_pin.off()
            time.sleep(delay / 2)  # Half the delay for the step off time
            self.encoder.update()
        # Ensure that the stepper motor is stopped when done
        self.step_pin.off()
        self.enable_motor(False)

    def move(self):
        # we use the fixed delay
        #print("Performing move...")
        self.step_pin.on()
        time.sleep(self.delay/2)  # ensure it doesn't move so fast
        self.step_pin.off()
        #time.sleep(self.delay/2)  
        self.encoder.update()

        #TODO: return true if move was successful. So, motor has to be aware of its position? Does it?

##Use this for testing
#motor = Motor()
#motor.enable_motor(True)
#while True:
#    motor = Motor()
    #motor.move_half_turn(20000, 120) #half a full turn is 10000 steps, 120seconds is 2 minutes.
#    motor.move()
#    motor.get_grating_angle()
