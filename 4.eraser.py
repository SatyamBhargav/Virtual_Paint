import cv2
import numpy as np
import time

load = True
if load:
    orange = np.load('np array\ColorVal.npy')

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

pen = cv2.resize(cv2.imread('image\pen2.png',1),(50,50))
eraser = cv2.resize(cv2.imread('image\eraser.png',1),(50,50))

kernel = np.ones((5,5),np.uint8)

#Making window size adjustable
cv2.namedWindow('image',cv2.WINDOW_NORMAL)

noiseth = 800
canvas = None
x1,y1 = 0,0
clear = False

bgobject = cv2.createBackgroundSubtractorMOG2(detectShadows= False)
bg_threshold = 600

switch = 'Pen'
last_switch = time.time()

while True:
    _,img = cap.read()
    frame = cv2.flip(img,1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    top_left = frame[0: 50, 0: 50]
    fgmask = bgobject.apply(top_left)

    switch_thresh = np.sum(fgmask==255)

    if switch_thresh > bg_threshold and (time.time() - last_switch) > 1:
    # Save the time of the switch.

        last_switch = time.time()

        if switch == 'Pen':
            switch = 'Eraser'
        else:
            switch = 'Pen'


    framehsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lower = orange[0]
    upper = orange[1]

    mask = cv2.inRange(framehsv,lower,upper)

    contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if contours and cv2.contourArea(max(contours, key = cv2.contourArea)) > noiseth:
        c = max(contours,key= cv2.contourArea)

        # Get bounding box coordinates around that contour
        x2,y2,w,h = cv2.boundingRect(c)

        area = cv2.contourArea(c)

        if x1 == 0 and y1 ==0:
            x1,y1 = x2,y2
        else:
            if switch == 'Pen':
                canvas = cv2.line(canvas,(x1,y1),(x2,y2),(57,255,20),10)
            else:
                cv2.circle(canvas, (x2,y2),20,(0,0,0),-1)

        x1,y1 = x2,y2

        if area > 25000:
            cv2.putText(canvas,'Cleaning',(100,200),cv2.FONT_HERSHEY_SIMPLEX,2, (0,0,255), 5, cv2.LINE_AA)
            clear = True


    else:
        x1,y1 = 0,0

    _,mask = cv2.threshold(cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY), 20,255, cv2.THRESH_BINARY)
    foreground = cv2.bitwise_and(canvas, canvas, mask=mask)
    background = cv2.bitwise_and(frame, frame,mask = cv2.bitwise_not(mask))
    frame = cv2.add(foreground, background)

    if switch != 'Pen':
        cv2.circle(frame, (x1, y1), 20, (255, 255, 255), -1)
        frame[0: 50, 0: 50] = eraser

    else:
        frame[0: 50, 0: 50] = pen

    cv2.imshow('image', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
# When c is pressed clear the canvas
    if clear:
        time.sleep(1)
        canvas = None

        clear = False
        switch = 'Pen'


cv2.destroyAllWindows()
cap.release()


