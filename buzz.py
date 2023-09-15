import RPi.GPIO as GPIO
import time
BUZ = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUZ, GPIO.OUT)

def beep_on():
    GPIO.output(BUZ, GPIO.HIGH)

def beep_off():
    GPIO.output(BUZ, GPIO.LOW)

if __name__ == '__main__':
    try:
        beep_on()
        time.sleep(0.1)
        beep_off()
        beep_on()
        time.sleep(0.1)
        beep_off()
        beep_on()
        time.sleep(0.1)
        beep_off()
        beep_on()
        time.sleep(0.5)
        beep_off()
        time.sleep(0.5)
        beep_off()
        beep_on()
        time.sleep(0.1)
        beep_off()
        beep_on()
        time.sleep(0.1)
        beep_off()
        beep_on()
        time.sleep(0.1)
        beep_off()
        
        
    except KeyboardInterrupt:
        GPIO.cleanup()
