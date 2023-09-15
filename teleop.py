import curses
import time
from PCA9685 import PCA9685
from AlphaBot2 import AlphaBot2

# Pan and tilt object
pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

# Alphabot motor object
Ab = AlphaBot2()

# Curses keyboard input settings
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
    while True:
        char = screen.getch()
            
        # Drivetrain motors teleoperation - WASD keys
        if char == ord('w'):
            Ab.forward(40)
        elif char == ord('a'):
            Ab.left(40)
        elif char == ord('s'):
            Ab.backward(40)
        elif char == ord('d'):
            Ab.right(40)
        elif char == ord(' '):
            Ab.stop()
            
finally:
    curses.nocbreak(); screen.keypad(0); curses.echo(0); curses.endwin()