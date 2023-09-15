import os
import cv2
import gc
from multiprocessing import Process, Manager

def write(stack, cam, top: int) -> None:
    print("Process to write: %s" % os.getpid())
    cap = cv2.VideoCapture(cam)
    while True:
        _, img = cap.read()
        if _:
            stack.append(img)
            
        if len(stack) >= top:
            del stack[:]
            gc.collect()
            
def read(stack) -> None:
    print("Process to read: %s" % os.getpid())
    while True:
        if len(stack) != 0:
            value = stack.pop()
            cv2.imshow("img", value)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            
if __name__ == '__main__':
    
    q = Manager().list()
    pw = Process(target=write, args=(q, 0, 100))
    pr = Process(target=read, args=(q,))
    
    pw.start()
    pr.start()
    pr.join()
    pw.terminate()