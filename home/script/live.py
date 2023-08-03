import cv2
import numpy as np
import sys
def fileNameExtract(path):
    if (path): 
        flag = False
        for i in range(len(path)-1, -1, -1):
            if path[i] == '/' or path[i] == '\\':
                flag = True
                break

        if flag:
            return path[i+1:]
    raise Exception('fail to extract file name')

def skinUnderTone():
    
    cascPath = "/Users/johnz/Documents/Hackabull/env/lib/python3.10/site-packages/cv2/data/haarcascade_frontalface_alt.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    video_capture = cv2.VideoCapture(0)

    lower = np.array([0, 48, 80], dtype = "uint8")
    upper = np.array([20, 255, 255], dtype = "uint8")
    while True:
        ret, img = video_capture.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        skinMask = cv2.inRange(converted, lower, upper)
        # apply a series of erosions and dilations to the mask
        # using an elliptical kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        skinMask = cv2.erode(skinMask, kernel, iterations = 1)
        skinMask = cv2.dilate(skinMask, kernel, iterations = 1)
        # blur the mask to help remove noise, then apply the
        # mask to the frame
        skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)

        skin = cv2.bitwise_and(img, img, mask = skinMask)

        cv2.imshow("hi",np.hstack([img, skin]))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

skinUnderTone()