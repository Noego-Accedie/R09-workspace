# Test program to count N20 encoder pulses with motor moving
import time
import signal
import sys
import RPi.GPIO as GPIO
import curses
from PCA9685 import PCA9685
from AlphaBot2 import AlphaBot2

# Motor control pins of DRV8833
IN1 = 20
IN2 = 16
# Encoder pins
C1 = 23
C2 = 24

# Alphabot motor object
Ab = AlphaBot2()

# Curses keyboard input settings
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
speed = 30

# Encoder pulses counter
C1count = 0
C2count = 0

    
# Interrupt routine when encoder pin C1 has event
# To be assigned in main program
def c1_callback(channel):
    global C1count
    C1count += 1
    print("C1 event: ", C1count)
    
# Interrupt routine when encoder pin C2 has event
# To be assigned in main program
def c2_callback(channel):
    global C2count
    C2count += 1
    print("C2 event: ", C2count)


try:
    GPIO.setmode(GPIO.BCM)
    # Setup GPIO input and output
    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Encoder C1 pin
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Encoder C2 pin
    GPIO.setup(IN1, GPIO.OUT) # Conneted to AIN2 of DRV8833
    GPIO.setup(IN2, GPIO.OUT) # Conneted to AIN2 of DRV8833

    # Set both motor pins LOW at the beginning
    # Ensure motor stop
    GPIO.output(IN1, GPIO.LOW) # Set AIN1
    GPIO.output(IN2, GPIO.LOW) # Set AIN1

    # Set up PWM for the pins
    # Both pins from one motor are used for both direction
    # This is specific to DRV8833, the driver in Alphabot will be different
    PWMA1 = GPIO.PWM(IN1, 50) # Use 500Hz
    PWMA2 = GPIO.PWM(IN2, 50) # Use 500Hz

    GPIO.add_event_detect(C1, GPIO.RISING, callback=c1_callback, bouncetime=100) # Setup callback for C1 rising pulse detected, bouncetime is for debouncing
    GPIO.add_event_detect(C2, GPIO.RISING, callback=c2_callback, bouncetime=100) # Setup callback for C2 rising pulse detected, bouncetime is for debouncing
    #GPIO.add_event_detect(C1, GPIO.RISING, callback=c1_callback) # Setup callback for C1 rising pulse detected
    #GPIO.add_event_detect(C2, GPIO.RISING, callback=c2_callback) # Setup callback for C2 rising pulse detected

    while True:
        char = screen.getch()
            
        # Drivetrain motors teleoperation - WASD keys
        if char == ord('w'):
            Ab.forward(speed)
        elif char == ord('a'):
            Ab.left(speed * 0.8)
        elif char == ord('s'):
            Ab.backward(speed)
        elif char == ord('d'):
            Ab.right(speed * 0.8)
        elif char == ord('e'):
            Ab.stop()

            
        print("C1 event: ", C1count)
        print("C2 event: ", C2count)


finally:
    curses.nocbreak(); screen.keypad(0); curses.echo(0); curses.endwin(); GPIO.remove_event_detect(C1); GPIO.remove_event_detect(C2); GPIO.cleanup()



'''
# Interrupt routine when user pressed Ctrl+C
# To be assigned in main program
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
'''

'''
if __name__ == '__main__':
    
    GPIO.setmode(GPIO.BCM)
    # Setup GPIO input and output
    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Encoder C1 pin
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Encoder C2 pin
    GPIO.setup(IN1, GPIO.OUT) # Conneted to AIN2 of DRV8833
    GPIO.setup(IN2, GPIO.OUT) # Conneted to AIN2 of DRV8833

    # Set both motor pins LOW at the beginning
    # Ensure motor stop
    GPIO.output(IN1, GPIO.LOW) # Set AIN1
    GPIO.output(IN2, GPIO.LOW) # Set AIN1

    # Set up PWM for the pins
    # Both pins from one motor are used for both direction
    # This is specific to DRV8833, the driver in Alphabot will be different
    PWMA1 = GPIO.PWM(IN1, 500) # Use 500Hz
    PWMA2 = GPIO.PWM(IN2, 500) # Use 500Hz
    
    # GPIO.add_event_detect(C1, GPIO.RISING, callback=c1_callback, bouncetime=100) # Setup callback for C1 rising pulse detected, bouncetime is for debouncing
    # GPIO.add_event_detect(C2, GPIO.RISING, callback=c2_callback, bouncetime=100) # Setup callback for C2 rising pulse detected, bouncetime is for debouncing
    GPIO.add_event_detect(C1, GPIO.RISING, callback=c1_callback) # Setup callback for C1 rising pulse detected
    GPIO.add_event_detect(C2, GPIO.RISING, callback=c2_callback) # Setup callback for C2 rising pulse detected
    
    # signal.signal(signal.SIGINT, signal_handler) # Setup callback for Ctrl+C
    # signal.pause()
    
    # Drive the motor clockwise
    PWMA1.stop() # Start PWM at his pin at 50% duty cycle
    PWMA2.start(12)
    # Use PWM.ChangeDutyCycle(duty cycle) if we want to change the speed in between

    # Wait 5 seconds
    time.sleep(5)

    # Stop the motor
    PWMA1.stop()
    PWMA2.stop()

    GPIO.cleanup()
    sys.exit(0)
    '''