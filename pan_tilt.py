import curses
import time
from PCA9685 import PCA9685

# Pan and tilt object
pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

# Tilt settings (up and down)
tilt_channel = 1
tilt_pulse = 1200
tilt_pulse_step = 30

# Pan settings (left and right)
pan_channel = 0
pan_pulse = 1700
pan_pulse_step = 30

# Curses keyboard input settings
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
    while True:
        char = screen.getch()
        
        # Pan and tilt operation - arrow keys
        if char == curses.KEY_UP:
            pwm.setServoPulse(tilt_channel, tilt_pulse - tilt_pulse_step)
            tilt_pulse -= tilt_pulse_step
        elif char == curses.KEY_DOWN:
            pwm.setServoPulse(tilt_channel, tilt_pulse + tilt_pulse_step)
            tilt_pulse += tilt_pulse_step
        elif char == curses.KEY_RIGHT:
            pwm.setServoPulse(pan_channel, pan_pulse - pan_pulse_step)
            pan_pulse -= pan_pulse_step
        elif char == curses.KEY_LEFT:
            pwm.setServoPulse(pan_channel, pan_pulse + pan_pulse_step)
            pan_pulse += pan_pulse_step
        elif char == ord('x'):
            pan_pulse = 1700
            pwm.setServoPulse(pan_channel, pan_pulse)
            tilt_pulse = 1200
            pwm.setServoPulse(tilt_channel, tilt_pulse)
            
finally:
    curses.nocbreak(); screen.keypad(0); curses.echo(0); curses.endwin()
