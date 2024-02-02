import serial
import time

# Replace 'COM_PORT' with your device file '/dev/tty.usbserial-A900LFQY'
ser = serial.Serial('/dev/tty.usbserial-A900LFQY', 9600, timeout=1)

with open('incoming_data.txt', 'w') as file:
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').rstrip()
                print("Received data:", data)
                file.write(data + '\n')
            time.sleep(0.1)
    except KeyboardInterrupt:
        ser.close()
