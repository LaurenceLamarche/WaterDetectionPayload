from machine import PWM, Pin
class LED:
    def __init__(self, led_num):
        if led_num == 1:
            
            self.wavelength = 1050
            self.pwm_pin = PWM(Pin(12))
            self.pwm_pin.freq(400)
            self.pwm_pin.duty_u16(65535) 
            self.adc_addr = 0
            
        elif led_num == 2:
            self.wavelength = 1200
            #self.pwm_pin = PWM(Pin(11))
            self.pwm_pin = PWM(Pin(15))
            self.pwm_pin.freq(400)
            self.pwm_pin.duty_u16(65535)
            self.adc_addr = 2
            
        elif led_num == 3:
            self.wavelength = 1200
            #self.pwm_pin = PWM(Pin(11))
            self.pwm_pin = PWM(Pin(15))
            self.pwm_pin.freq(400)
            self.pwm_pin.duty_u16(65535)
            self.adc_addr = 2
            
        elif led_num == 4:
            self.wavelength = 1550
            self.pwm_pin = PWM(Pin(13))
            self.pwm_pin.freq(400)
            self.pwm_pin.duty_u16(65535)
            self.adc_addr = 1
