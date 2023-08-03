import cv2
import numpy as np
import sys
from .setup import CASC_PATH
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

def skinUnderTone(imgPath, pathToWrite=None):
    faceCascade = cv2.CascadeClassifier(CASC_PATH)
    
    img = cv2.imread(imgPath,)
    try:
        fileName = fileNameExtract(imgPath)
    except:
        fileName = imgPath
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
    
    lower = np.array([0, 48, 80], dtype = "uint8")
    upper = np.array([20, 255, 255], dtype = "uint8")

    converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)

    # apply a series of erosions and dilations to the mask
    # using an elliptical kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinMask = cv2.erode(skinMask, kernel, iterations = 1)
    skinMask = cv2.dilate(skinMask, kernel, iterations = 1)
    # blur the mask to help remove noise, then apply the
    # mask to the frame
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    # np.set_printoptions(threshold=sys.maxsize)
    # print(skinMask)
    # print(len(skinMask))
    # print(len(skinMask[0]))
    # sumRGB = [0,0,0]
    # for i,row in enumerate(skinMask):
    #     for j,pixel in enumerate(row):
    #         if pixel != 0:
    #             (b, g, r) = img[i][j]
    #             # print(img[i][j])
    #             # print(skinMask[i][j])
    #             # print(i,j)
    #             sumRGB[0] += b
    #             sumRGB[1] += g
    #             sumRGB[2] += r
    # brightness = sum(sumRGB)/3
    # if brightness == 0:
    #     raise("no skin detected")
    # bR=sumRGB[0]/brightness
    # gR=sumRGB[1]/brightness
    # rR=sumRGB[2]/brightness

    # print(f"{fileName}\tb: {round(bR,2)}\tg: {round(gR,2)}\tr: {round(rR,2)}")

    skin = cv2.bitwise_and(img, img, mask = skinMask)
    count = 0
    total = [0, 0 , 0]
    for i,row in enumerate(skin):
        for j,pixel in enumerate(row):
            b, g, r = pixel
            # print(j,i)
            # print(b, g, r)
            average = sum(pixel)/3
            if average == 0:
                continue
            total[0] += b/average
            total[1] += g/average
            total[2] += r/average
            count += 1
    if count == 0:
        print(f"{fileName} No Skin Detected")
    else:
        bValue = round(total[0]/count,2)
        gValue = round(total[1]/count,2)
        rValue = round(total[2]/count,2)
        print(f"new: {fileName}\tb: {bValue}\tg: {gValue}\tr: {rValue}")
        diff = round(total[1]/count,2) - round(total[0]/count,2)
        print(f"diff:{diff}")

    faceFound = False
    for (x, y, w, h) in faces:
        # x = round(x/2)
        # y = round(y/2)
        # w = round(w/2)
        # h = round(h/2)
        # crop_img = img[y:y+h-100, x:x+w-100]
        crop_img = img[y:y+h, x:x+w]
        faceFound = True
    #     sumRGB = [0,0,0]
    #     for x in crop_img:
    #         for (r, g, b) in x:
    #             # print(r,g,b)
    #             sumRGB[0] += b
    #             sumRGB[1] += g
    #             sumRGB[2] += r
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
    #     # avg_color_per_row = np.average(crop_img, axis=0)
    #     # avg_color = np.average(avg_color_per_row, axis=0)
    #     # print(avg_color)
    #     print(sumRGB)
    #     print(f"r: {sumRGB[0]*3/sum(sumRGB)}, g: {sumRGB[1]*3/sum(sumRGB)}, b: {sumRGB[2]*3/sum(sumRGB)}  /")
        # img = crop_img
    cv2.imwrite("home/static/userview.jpg", img)

    # show the skin in the image along with the mask
    if pathToWrite is None or False:
        cv2.imshow("images", np.hstack([img, skin]))
        cv2.waitKey()
    else:
        cv2.imwrite("home/static/debug.jpg", skin)
    
    try: 
        if bValue >= 0.85 and diff < 0.12:
            verdict = 0
            raise("")
        if bValue >= 0.75 and diff <= 0.9:
            verdict = 1
            raise("")
        if diff >= 0.15 and bValue <0.80:
            verdict = 2
            raise("")
        if bValue <0.80:
            verdict = 2
            raise("")
        if diff > 15:
            verdict = 2
            raise("")
        if diff <= 15 and bValue<0.85:
            verdict = 2
            raise("")
    except:
        if count == 0:
            verdict = -1
    return verdict, faceFound
    # im_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    # skin_ycrcb_mint = np.array((0, 133, 77))
    # skin_ycrcb_maxt = np.array((255, 173, 127))
    # skin_ycrcb = cv2.inRange(im_ycrcb, skin_ycrcb_mint, skin_ycrcb_maxt)

    # cv2.imshow("skin",skin_ycrcb )
    # cv2.waitKey()
    # contours, _ = cv2.findContours(skin_ycrcb, cv2.RETR_EXTERNAL, 
    #         cv2.CHAIN_APPROX_SIMPLE)
    # for i, c in enumerate(contours):
    #     area = cv2.contourArea(c)
    #     if area > 1000:
    #         cv2.drawContours(img, contours, i, (255, 0, 0), 3)
    # # cv2.imwrite(sys.argv[3], im)         # Final image
    # cv2.imshow("final",img )
    # cv2.waitKey()

#     # video_capture = cv2.VideoCapture(0)
#     # while False:
#     #     ret, img = video_capture.read()
#     #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     #     faces = faceCascade.detectMultiScale(
#     #         gray,
#     #         scaleFactor=1.1,
#     #         minNeighbors=5,
#     #         minSize=(30, 30),
#     #         flags = cv2.CASCADE_SCALE_IMAGE
#     #     )
            
        
#     #     faceFound = False
#     #     for (x, y, w, h) in faces:
#     #         crop_img = img[y:y+h, x:x+w]
#     #         faceFound = True
#     #         cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     #         # avg_color_per_row = np.average(crop_img, axis=0)
#     #         # avg_color = np.average(avg_color_per_row, axis=0)
#     #         # print(avg_color)
#     # # a = []
#     # # for i in range(200):
#     # #     row = []
#     # #     for y in range(200):
#     # #         row.append(avg_color)
#     # #     a.append(row)

#     # # a = np.array(a)
#     # # a = a.round()
#     # # print(a)
#     # # print(faces)
#     # # print(crop_img)
#     # # cv2.namedWindow("hi",cv2.WINDOW_AUTOSIZE)
#     #     if faceFound:
#     #         cv2.imshow("Faces found", crop_img)
#     #     else:
#     #         cv2.imshow("Faces not found", img)
    
    
#     #     if cv2.waitKey(1) & 0xFF == ord('q'):
#     #         break
#     # video_capture.release()
#     cv2.destroyAllWindows()

#     # print(img)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)

if __name__ == "__main__":
    try:
        imgPath = sys.argv[1]
        skinUnderTone(imgPath)
    except:
        import os
        arr = os.listdir()
        for imgPath in arr:
            if imgPath[-3:] == "jpg":
                skinUnderTone(imgPath,False)

        

# im = cv2.imread(sys.argv[1])
# gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# cv2.imshow("gray", gray)
# # cv2.waitKey()
# cv2.imshow("ori", im)
# cv2.waitKey()


# im = cv2.imread(sys.argv[1])
# im_ycrcb = cv2.cvtColor(im, cv2.COLOR_BGR2YCR_CB)

# skin_ycrcb_mint = np.array((0, 133, 77))
# skin_ycrcb_maxt = np.array((255, 173, 127))
# skin_ycrcb = cv2.inRange(im_ycrcb, skin_ycrcb_mint, skin_ycrcb_maxt)
# print(skin_ycrcb)


# # cv2.imwrite(sys.argv[2], skin_ycrcb) # Second image
# cv2.imshow("skin",skin_ycrcb )
# cv2.waitKey()
# contours, _ = cv2.findContours(skin_ycrcb, cv2.RETR_EXTERNAL, 
#         cv2.CHAIN_APPROX_SIMPLE)
# for i, c in enumerate(contours):
#     area = cv2.contourArea(c)
#     if area > 1000:
#         cv2.drawContours(im, contours, i, (255, 0, 0), 3)
# # cv2.imwrite(sys.argv[3], im)         # Final image
# cv2.imshow("final",im )
# cv2.waitKey()

    