import cv2
import pickle
import numpy as np
import cvzone

# cap1 = cv2.VideoCapture()
cap = cv2.VideoCapture(2)

with open("carparkpos", "rb") as f:
    Position_list = pickle.load(f)

WIDTH , HEIGHT = 80 , 110


def CheckParkingSpace(imgPro):

    spaceCounter = 0


    for pos in Position_list:
        x,y = pos
        # cv2.rectangle(img,pos,(pos[0]+WIDTH,pos[1]+HEIGHT),(155,0,255),2)
        imgCrop = imgPro[y:y+HEIGHT,x:x+WIDTH]
        # cv2.imshow(str(x*y),imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+HEIGHT-2),scale=1,thickness=1,offset=2, colorR=(0,0,255))

        if count < 650:
            color = (0,255,0) #green
            thickness = 3
            spaceCounter += 1
        else:
            color = (0,0,255) #red
            thickness = 2

        cv2.rectangle(img,pos,(pos[0]+WIDTH,pos[1]+HEIGHT),color,thickness)
    cvzone.putTextRect(img,f'{"Free="}{(spaceCounter)}/{len(Position_list)}',(6,35),scale=1.5,thickness=2,font=cv2.FONT_HERSHEY_COMPLEX,offset=3,
                       colorR=(8, 255, 246),colorT=(0, 0, 0))
# , colorR=(155,0,255)
while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success , img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV,25,16)
    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.ones((3,3),np.uint8)
    imgDilation = cv2.dilate(imgMedian, kernel,iterations=1)



    CheckParkingSpace(imgDilation)
    # for pos in Position_list:
    #     cv2.rectangle(img,pos,(pos[0]+WIDTH,pos[1]+HEIGHT),(155,0,255),2)
    cv2.imshow("image",img)
    # cv2.imshow("imageThreshold",imgThreshold)
    # cv2.imshow("imageBlur",imgBlur)
    # cv2.imshow("imageMedian",imgMedian)
    # cv2.imshow("imageDilation",imgDilation)
    cv2.waitKey(15)