import serial
import time

uart_id = 0
baud_rate = 115200
ser = serial.Serial('/dev/tty.usbserial-A900LFQY', baud_rate, timeout=1)

def change_duty_cycle(duty_cycle):
    # Send duty cycle command as bytes
    command = f"{duty_cycle}\n".encode()
    print("sending duty cycle as: ", duty_cycle)
    ser.write(command)


try:
    # Change duty cycle in a loop or based on user input
    while True:
        duty_cycle_percent = input("Enter duty cycle percent (0.0 - 1.0): ")
        duty_cycle_int = int(65535*float(duty_cycle_percent))
        change_duty_cycle(duty_cycle_int)
        time.sleep(1)  # Adjust delay as needed
except KeyboardInterrupt:
    pass
finally:
    ser.close()