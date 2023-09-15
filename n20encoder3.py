# Test program to count N20 encoder pulses with motor moving
import time
import signal
import sys
import RPi.GPIO as GPIO
import curses
from PCA9685 import PCA9685
from AlphaBot2 import AlphaBot2

# Motor control pins of DRV8833
motor1 = 19
motor2 = 24
# Encoder pins
encoder1 = 21
encoder2 = 23

# Alphabot motor object
Ab = AlphaBot2()

# Curses keyboard input settings
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
speed = 30

# Encoder pulses counter
encoder1Count = 0
encoder2Count = 0

    
# Interrupt routine when encoder pin encoder1 has event
# To be assigned in main program
def encoder1_callback(channel):
    global encoder1Count
    encoder1Count += 1
    print("encoder1 event: ", encoder1Count)
    
# Interrupt routine when encoder pin encoder2 has event
# To be assigned in main program
def encoder2_callback(channel):
    global encoder2Count
    encoder2Count += 1
    print("encoder2 event: ", encoder2Count)


try:
    GPIO.setmode(GPIO.BOARD)
    # Setup GPIO input and output
    GPIO.setup(encoder1, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Encoder encoder1 pin
    GPIO.setup(encoder2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Encoder encoder2 pin
    GPIO.setup(motor1, GPIO.OUT) # Conneted to AIN2 of DRV8833
    GPIO.setup(motor2, GPIO.OUT) # Conneted to AIN2 of DRV8833

    # Set both motor pins LOW at the beginning
    # Ensure motor stop
    GPIO.output(motor1, GPIO.LOW) # Set AIN1
    GPIO.output(motor2, GPIO.LOW) # Set AIN1

    # Set up PWM for the pins
    # Both pins from one motor are used for both direction
    # This is specific to DRV8833, the driver in Alphabot will be different
    PWM1 = GPIO.PWM(motor1, 50) # Use 500Hz
    PWM2 = GPIO.PWM(motor2, 50) # Use 500Hz

    GPIO.add_event_detect(encoder1, GPIO.RISING, callback=encoder1_callback, bouncetime=100) # Setup callback for encoder1 rising pulse detected, bouncetime is for debouncing
    GPIO.add_event_detect(encoder2, GPIO.RISING, callback=encoder2_callback, bouncetime=100) # Setup callback for encoder2 rising pulse detected, bouncetime is for debouncing
    #GPIO.add_event_detect(encoder1, GPIO.RISING, callback=c1_callback) # Setup callback for encoder1 rising pulse detected
    #GPIO.add_event_detect(encoder2, GPIO.RISING, callback=c2_callback) # Setup callback for encoder2 rising pulse detected

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

            
        print("encoder1 event: ", encoder1Count)
        print("encoder2 event: ", encoder2Count)


finally:
    curses.nocbreak(); screen.keypad(0); curses.echo(0); curses.endwin(); GPIO.remove_event_detect(encoder1); GPIO.remove_event_detect(encoder2); GPIO.cleanup()



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
    GPIO.setup(encoder1, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Encoder encoder1 pin
    GPIO.setup(encoder2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Encoder encoder2 pin
    GPIO.setup(motor1, GPIO.OUT) # Conneted to AIN2 of DRV8833
    GPIO.setup(motor2, GPIO.OUT) # Conneted to AIN2 of DRV8833

    # Set both motor pins LOW at the beginning
    # Ensure motor stop
    GPIO.output(motor1, GPIO.LOW) # Set AIN1
    GPIO.output(motor2, GPIO.LOW) # Set AIN1

    # Set up PWM for the pins
    # Both pins from one motor are used for both direction
    # This is specific to DRV8833, the driver in Alphabot will be different
    PWM1 = GPIO.PWM(motor1, 500) # Use 500Hz
    PWM2 = GPIO.PWM(motor2, 500) # Use 500Hz
    
    # GPIO.add_event_detect(encoder1, GPIO.RISING, callback=c1_callback, bouncetime=100) # Setup callback for encoder1 rising pulse detected, bouncetime is for debouncing
    # GPIO.add_event_detect(encoder2, GPIO.RISING, callback=c2_callback, bouncetime=100) # Setup callback for encoder2 rising pulse detected, bouncetime is for debouncing
    GPIO.add_event_detect(encoder1, GPIO.RISING, callback=c1_callback) # Setup callback for encoder1 rising pulse detected
    GPIO.add_event_detect(encoder2, GPIO.RISING, callback=c2_callback) # Setup callback for encoder2 rising pulse detected
    
    # signal.signal(signal.SIGINT, signal_handler) # Setup callback for Ctrl+C
    # signal.pause()
    
    # Drive the motor clockwise
    PWM1.stop() # Start PWM at his pin at 50% duty cycle
    PWM2.start(12)
    # Use PWM.ChangeDutyCycle(duty cycle) if we want to change the speed in between

    # Wait 5 seconds
    time.sleep(5)

    # Stop the motor
    PWM1.stop()
    PWM2.stop()

    GPIO.cleanup()
    sys.exit(0)
    '''