''' Trying opencv library to detect motion'''


import numpy as np
import cv2
import cv


cap = cv2.VideoCapture(0)
body_cascade = cv2.CascadeClassifier('<?xml/home/zarin/Documents/SoftDes/haarcascade_fullbody.xml>')
kernel = np.ones((21,21),'uint8')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    body = body_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))

    for (x,y,w,h) in body:
        frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel)




    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


