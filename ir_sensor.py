import RPi.GPIO as GPIO
import time
from AlphaBot2 import AlphaBot2

#Ab = AlphaBot2() #Initialize AlphaBot2

DR = 19 #IR right sensor to detect obstacles
DL = 16 #IR left sensor to detect obstacles

GPIO.setmode(GPIO.BCM) #Set to use Broadcom SOC pin numbering system
GPIO.setwarnings(False) #Turn off warning if the pin is being used
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP) #Set DL as Input pin and set as pull-up
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP) #Set DR as Input pin and set as pull-up

if __name__ == "__main__":
    try:
        while True:
            DR_status = GPIO.input(DR)
            DL_status = GPIO.input(DL)
            
            if ((DL_status == 0) and (DR_status == 0)):
                #when DL and DR status are 0
                #this indicate that an obstacle is detected
                #the robot should "stop" because an obstacle is in the way
                print("obstacle on the left and right side") 
            elif ((DL_status == 0) and (DR_status != 0)):
                #when DL is 0 and DR is not 0
                #this indicate that an obstacle is detected on its left side
                print("obstacle on the left side")
            elif ((DL_status != 0) and (DR_status == 0)):
                #when DL is not 0 and DR is 0
                #this indicate that an obstacle is detected on its right side
                print("obstacle on the right side")
            else:
                #when DL and DR is not 0
                #this indicate that no obstacle is detected
                print("no obstacle")
    except KeyboardInterrupt:
        GPIO.cleanup() #clean up used resources