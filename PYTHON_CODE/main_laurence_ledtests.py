from machine import Pin, PWM
import time

Create a PWM object on a GPIO pin
pwm_pin = PWM(Pin(15))  # Replace 15 with the GPIO pin number you want to use

Set the PWM frequency (e.g., 1000Hz)
pwm_pin.freq(1000)

Set the duty cycle (range from 0 to 65535, e.g., 30% duty cycle)
pwm_pin.duty_u16(19660)

# To change the duty cycle (e.g., to 75%)
# pwm_pin.duty_u16(49152)

#To stop PWM
#pwm_pin.deinit()