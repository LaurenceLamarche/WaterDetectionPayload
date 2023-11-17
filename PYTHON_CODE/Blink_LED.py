import machine
import utime

# Define the built-in LED pin (GPIO 25 on the Raspberry Pi Pico)
led = machine.Pin(25, machine.Pin.OUT)

# Function to blink the LED
def blink_led(times, interval):
    for _ in range(times):
        led.value(1)  # Turn the LED on
        utime.sleep(interval)  # Wait for 'interval' seconds
        led.value(0)  # Turn the LED off
        utime.sleep(interval)  # Wait for 'interval' seconds

# Blink the LED 5 times with a 1-second interval
blink_led(5, 1)
