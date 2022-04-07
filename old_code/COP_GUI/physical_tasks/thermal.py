import cv2
import numpy as np
print(cv2.__version__)
capT = cv2.VideoCapture('/dev/video4')
capC = cv2.VideoCapture('/dev/video2')
capT.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('Y','1','6',' '))
capC.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('Y','1','6',' '))
capT.set(cv2.CAP_PROP_CONVERT_RGB, 0)

i = 0

while(True):
    ret, frameT = capT.read()
    retC, frameC = capC.read()
    frameT = np.array(frameT, dtype=np.float)

    minVal = frameT.min()
    maxVal = frameT.max()

    frameT = (frameT - minVal)/(maxVal - minVal)
    cv2.imshow('frameT', frameT)
    cv2.imshow('frameC', frameC)

    pathC = '/home/heracleia/Desktop/color/' + str(i) + '.jpg'
    pathT = '/home/heracleia/Desktop/thermal/' + str(i) + '.jpg'
    # cv2.imwrite(pathC, frameC)
    # cv2.imwrite(pathT, frameT*255)
    i += 1
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

capC.release()
capT.release()
cv2.destroyAllWindows()