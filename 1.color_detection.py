import cv2
import numpy as np

def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.createTrackbar('HUE Min','HSV',0,179,empty)
cv2.createTrackbar('HUE Max','HSV',179,179,empty)
cv2.createTrackbar('SAT Min','HSV',0,255,empty)
cv2.createTrackbar('SAT Max','HSV',255,255,empty)
cv2.createTrackbar('VAL Min','HSV',0,255,empty)
cv2.createTrackbar('VAL Max','HSV',255,255,empty)


cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)


while True:
    _, img2 = cap.read()
    img = cv2.flip(img2,1)

    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos('HUE Min','HSV')
    h_max = cv2.getTrackbarPos('HUE Max', 'HSV')
    s_min = cv2.getTrackbarPos('SAT Min', 'HSV')
    s_max = cv2.getTrackbarPos('SAT Max', 'HSV')
    v_min = cv2.getTrackbarPos('VAL Min', 'HSV')
    v_max = cv2.getTrackbarPos('VAL Max', 'HSV')


    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imghsv,lower,upper)
    result = cv2.bitwise_and(img,img, mask = mask)

    # Converting the binary mask to 3 channel image, this is just so
    # we can stack it with the others
    maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # stack the mask, original frame and the filtered result
    stacked = np.hstack((maskBGR,img,result))

    # Show this stacked frame at 35% of the size.
    cv2.imshow('HSV',cv2.resize(stacked,None,fx=0.35,fy=0.35))


    # If the user presses ESC then exit the program
    if cv2.waitKey(1) == 27:
        break

    # If the user presses `s` then print this array.
    if cv2.waitKey(1) & 0xFF == ord('s'):
        thearray = [lower,upper]
        print(thearray)

        np.save('np array\ColorVal.npy',thearray)
        break


cap.release()
cv2.destroyAllWindows()