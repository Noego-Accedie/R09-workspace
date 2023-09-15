import RPi.GPIO as GPIO
import time

class AlphaBot2(object):
    #self,ain1=12,ain2=13,ena=6,bin1=20,bin2=21,enb=26
    def __init__(self,ain1=12,ain2=13,ena=6,bin1=20,bin2=21,enb=26,enc1=10,enc2=8):
        self.AIN1 = ain1
        self.AIN2 = ain2
        self.BIN1 = bin1
        self.BIN2 = bin2
        self.ENA = ena
        self.ENB = enb
        self.ENC1 = enc1
        self.ENC2 = enc2
        self.PA  = 50
        self.PB  = 50

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.AIN1,GPIO.OUT)
        GPIO.setup(self.AIN2,GPIO.OUT)
        GPIO.setup(self.BIN1,GPIO.OUT)
        GPIO.setup(self.BIN2,GPIO.OUT)
        GPIO.setup(self.ENA,GPIO.OUT)
        GPIO.setup(self.ENB,GPIO.OUT)
        GPIO.setup(self.ENC1, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Encoder C1 pin
        GPIO.setup(self.ENC2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Encoder C2 pin  
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def forward(self, duty_cycle):
        self.PWMA.ChangeDutyCycle(duty_cycle + 1)
        self.PWMB.ChangeDutyCycle(duty_cycle)
        GPIO.output(self.AIN1,GPIO.LOW)
        GPIO.output(self.AIN2,GPIO.HIGH)
        GPIO.output(self.BIN1,GPIO.LOW)
        GPIO.output(self.BIN2,GPIO.HIGH)


    def stop(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.AIN1,GPIO.LOW)
        GPIO.output(self.AIN2,GPIO.LOW)
        GPIO.output(self.BIN1,GPIO.LOW)
        GPIO.output(self.BIN2,GPIO.LOW)

    def backward(self, duty_cycle):
        self.PWMA.ChangeDutyCycle(duty_cycle)
        self.PWMB.ChangeDutyCycle(duty_cycle)
        GPIO.output(self.AIN1,GPIO.HIGH)
        GPIO.output(self.AIN2,GPIO.LOW)
        GPIO.output(self.BIN1,GPIO.HIGH)
        GPIO.output(self.BIN2,GPIO.LOW)

        
    def left(self, duty_cycle):
        self.PWMA.ChangeDutyCycle(duty_cycle)
        self.PWMB.ChangeDutyCycle(duty_cycle)
        GPIO.output(self.AIN1,GPIO.HIGH)
        GPIO.output(self.AIN2,GPIO.LOW)
        GPIO.output(self.BIN1,GPIO.LOW)
        GPIO.output(self.BIN2,GPIO.HIGH)


    def right(self, duty_cycle):
        self.PWMA.ChangeDutyCycle(duty_cycle)
        self.PWMB.ChangeDutyCycle(duty_cycle)
        GPIO.output(self.AIN1,GPIO.LOW)
        GPIO.output(self.AIN2,GPIO.HIGH)
        GPIO.output(self.BIN1,GPIO.HIGH)
        GPIO.output(self.BIN2,GPIO.LOW)

    # Interrupt routine when encoder pin C1 has event
    # To be assigned in main program
    def encoder1_callback(channel):
        global encoder1Count
        encoder1Count += 1
        print("encoder1 event: ", encoder1Count)

    # Interrupt routine when encoder pin C2 has event
    # To be assigned in main program
    def encoder2_callback(channel):
        global encoder2Count
        encoder2Count += 1
        print("encoder2 event: ", encoder2Count)

    def allow_encoder_event(self):
        GPIO.add_event_detect(self.ENC1, GPIO.RISING, callback=self.encoder1_callback) # Setup callback for C1 rising pulse detected
        GPIO.add_event_detect(self.ENC2, GPIO.RISING, callback=self.encoder2_callback) # Setup callback for C2 rising pulse detected
        
    def setPWMA(self,value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def setPWMB(self,value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)  
        
    def setMotor(self, left, right):
        if((right >= 0) and (right <= 100)):
            GPIO.output(self.AIN1,GPIO.HIGH)
            GPIO.output(self.AIN2,GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif((right < 0) and (right >= -100)):
            GPIO.output(self.AIN1,GPIO.LOW)
            GPIO.output(self.AIN2,GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if((left >= 0) and (left <= 100)):
            GPIO.output(self.BIN1,GPIO.HIGH)
            GPIO.output(self.BIN2,GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif((left < 0) and (left >= -100)):
            GPIO.output(self.BIN1,GPIO.LOW)
            GPIO.output(self.BIN2,GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

# if __name__=='__main__':
#     Ab = AlphaBot2()
#     try:
#         Ab.right(10)
#         time.sleep(1)
#         Ab.left(10)
#         time.sleep(1.1)
#         Ab.stop()
#         #while True:
#         #    Ab.left(10)
#         #    time.sleep(1)
#     except KeyboardInterrupt:
#         Ab.stop()
#         GPIO.cleanup()
