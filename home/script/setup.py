CASC_PATH = "/Users/johnz/Documents/Hackabull/env/lib/python3.10/site-packages/cv2/data/haarcascade_frontalface_alt.xml"
# CASC_PATH = "/Users/johnz/Documents/Github/yourPalette/env/lib/python3.10/site-packages/cv2/data/haarcascade_frontalface_alt.xml"
import cv2
import os
newStr = cv2.__file__ + "/.././data/haarcascade_frontalface_alt.xml"
print(os.path.abspath(newStr))
CASC_PATH=os.path.abspath(newStr)

# if error with path, hard code your path
