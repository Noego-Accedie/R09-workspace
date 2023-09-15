import numpy as np
import time
import cv2

camera = cv2.VideoCapture(0)
time.sleep(2.0)

boundaries = [
    ([0, 0, 100], [50, 56, 255]), # red
    ([70, 120, 0], [100, 170, 40]), # green
    ([180, 50, 0], [200, 115, 40]) # blue
]

while True:
    okay, image = camera.read()
    image = cv2.resize(image, (400, 400))
    if not okay:
        continue
    
    # Create Numpy arrays from the boundaries
    lower1 = np.array(boundaries[0][0], dtype="uint8")
    upper1 = np.array(boundaries[0][1], dtype="uint8")
    
    lower2 = np.array(boundaries[1][0], dtype="uint8")
    upper2 = np.array(boundaries[1][1], dtype="uint8")
    
    lower3 = np.array(boundaries[2][0], dtype="uint8")
    upper3 = np.array(boundaries[2][1], dtype="uint8")
    
    mask1 = cv2.inRange(image, lower1, upper1)
    mask2 = cv2.inRange(image, lower2, upper2)
    mask3 = cv2.inRange(image, lower3, upper3)
    
    red_output = cv2.bitwise_and(image, image, mask = mask1)
    green_output = cv2.bitwise_and(image, image, mask = mask2)
    blue_output = cv2.bitwise_and(image, image, mask = mask3)
    
    if mask1.any():
        print("red!")
    if mask2.any():
        print("green!")
    if mask3.any():
        print("blue")
    else:
        print("None")
        
    cv2.imshow("images", np.hstack([image, red_output]))
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
      
camera.release()
cv2.destroyAllWindows()