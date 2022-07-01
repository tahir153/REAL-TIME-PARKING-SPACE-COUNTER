import cv2
import pickle


WIDTH , HEIGHT = 90 , 115

try:
    with open("carparkpos", "rb") as f:
        Position_list = pickle.load(f)
except:
    Position_list = []

def Mouse_Click(events,x,y,flags ,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        Position_list.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(Position_list):
            x1,y1 = pos
            if x1<x<x1+WIDTH and y1<y<y1+HEIGHT:
                Position_list.pop(i)

    with open("carparkpos","wb") as f:
        pickle.dump(Position_list,f)


while True:
    img = cv2.imread("PL.png")
    for pos in Position_list:
        cv2.rectangle(img,pos,(pos[0]+WIDTH,pos[1]+HEIGHT),(0,0,255),2)
    cv2.imshow("image",img)
    cv2.setMouseCallback("image",Mouse_Click)
    cv2.waitKey(10)