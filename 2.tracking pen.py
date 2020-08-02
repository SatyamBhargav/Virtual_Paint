import cv2
import numpy as np

load = True
if load:
    orange = np.load('np array\ColorVal.npy')

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

kernel = np.ones((5,5),np.uint8)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

noiseth = 500

while True:
    _,img = cap.read()
    frame = cv2.flip(img,1)

    framehsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lower = orange[0]
    upper = orange[1]

    mask = cv2.inRange(framehsv,lower,upper)

    contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    #in cv2.contourArea(max()) key is a function which will be applied on contours
    #key is a parameter of max() we can give any function to key

    #area of all contours will be find and then contour having max area will be selected and then againg its area will be produce
    #again using the same function area will be produce and will be stored into a variable "c".
    if contours and cv2.contourArea(max(contours, key = cv2.contourArea)) > noiseth:
        c = max(contours,key= cv2.contourArea)

        # Get bounding box coordinates around that contour
        x,y,w,h = cv2.boundingRect(c)

        # Draw that bounding box
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,25,255),2)

    cv2.imshow('image',frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()
cap.release()


